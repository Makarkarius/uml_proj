import sys

import requests
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFrame, QSplitter, QLabel, QLineEdit, QHBoxLayout, \
    QPushButton, QComboBox

from core import encoder
from core.model import Acts, LinkActs

links = ['использование', 'наследование', 'ничего']
acts = Acts()

class ActsFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.diagram = QPixmap('')

        self.topRight = QFrame()
        self.topRight.setFrameShape(QFrame.StyledPanel)
        self.botRight = QFrame()
        self.botRight.setFrameShape(QFrame.StyledPanel)


        self.leftFrame = QFrame()
        self.leftFrame.setFrameShape(QFrame.StyledPanel)

        self.labelLeft = QLabel("", self.leftFrame)
        self.labelLeft.setAlignment(Qt.AlignCenter)
        self.labelLeft.setPixmap(self.diagram)

        self.rightFrame = QFrame()
        self.rightFrame.setFrameShape(QFrame.StyledPanel)

        splitter2 = QSplitter(Qt.Horizontal)

        splitter2.addWidget(self.leftFrame)
        splitter2.addWidget(self.rightFrame)
        splitter2.setSizes([30, 14])

        hbox = QHBoxLayout(self)
        hbox.addWidget(splitter2)

        self.textbox_errors = QLineEdit("", self.rightFrame)
        self.textbox_errors.setReadOnly(True)
        self.textbox_errors.move(10, 300)
        self.textbox_errors.setFrame(False)
        font = QFont()
        font.setPointSize(11)
        self.textbox_errors.setFont(font)
        self.textbox_errors.setMinimumSize(15, 15)
        self.textbox_errors.setMaximumSize(300, 20)
        self.textbox_errors.resize(300, 20)

        self.textbox_errors.setStyleSheet('background-color: #f0f0f0; border: none; color: red;')

        self.setLayout(hbox)
        self.crt()


    def crt(self):
        self.system = QLineEdit(self.rightFrame)
        self.system.move(10, 5)
        self.system.resize(100, 20)
        self.system.setPlaceholderText('название системы')
        self.system.setText(acts.system_name)

        self.actor = QLineEdit(self.rightFrame)
        self.actor.move(10, 40)
        self.actor.resize(120, 20)
        self.actor.setPlaceholderText('эктор')
        self.actor_nick = QLineEdit(self.rightFrame)
        self.actor_nick.move(140, 40)
        self.actor_nick.setPlaceholderText('сокращение')
        self.actor_nick.resize(80, 20)
        self.actor_b = QPushButton('создать', self.rightFrame)
        self.actor_b.clicked.connect(self.add_actor)
        self.actor_b.move(230, 40)

        self.action = QLineEdit(self.rightFrame)
        self.action.move(10, 65)
        self.action.resize(120, 20)
        self.action.setPlaceholderText('действие')
        self.action_nick = QLineEdit(self.rightFrame)
        self.action_nick.move(140, 65)
        self.action_nick.setPlaceholderText('сокращение')
        self.action_nick.resize(80, 20)
        self.action_b = QPushButton('создать', self.rightFrame)
        self.action_b.clicked.connect(self.add_action)
        self.action_b.move(230, 65)

        self.actor_combo = QComboBox(self.rightFrame)
        for a in acts.actors:
            self.actor_combo.addItem(a[1])
        self.actor_combo.move(10, 95)
        self.actor_combo.resize(100, 20)
        self.del_actor = QPushButton('удалить эктора', self.rightFrame)
        self.del_actor.clicked.connect(self.delete_actor)
        self.del_actor.move(10, 120)
        self.del_actor.resize(100, 20)

        self.action_combo = QComboBox(self.rightFrame)
        for a in acts.actions:
            self.action_combo.addItem(a[1])
        self.action_combo.move(120, 95)
        self.action_combo.resize(100, 20)
        self.del_action = QPushButton('удалить действие', self.rightFrame)
        self.del_action.clicked.connect(self.delete_action)
        self.del_action.move(120, 120)
        self.del_action.resize(100, 20)

        ql = QLabel("связи", self.rightFrame)
        ql.move(10, 155)

        self.left = QComboBox(self.rightFrame)
        self.link = QComboBox(self.rightFrame)
        self.link.addItems(links)
        self.right = QComboBox(self.rightFrame)
        for a in acts.actors:
            self.left.addItem(a[1])
            self.left.addItem(a[1])
        for a in acts.actions:
            self.right.addItem(a[1])
            self.right.addItem(a[1])
        self.left.resize(90, 20)
        self.link.resize(90, 20)
        self.right.resize(90, 20)
        self.left.move(10, 180)
        self.link.move(110, 180)
        self.right.move(210, 180)
        self.comm = QLineEdit(self.rightFrame)
        self.comm.resize(90, 20)
        self.comm.move(110, 205)
        self.comm.setPlaceholderText('комм')
        self.link_b = QPushButton('добавить изменения', self.rightFrame)
        self.link_b.clicked.connect(self.edit_link)
        self.link_b.resize(120, 20)
        self.link_b.move(95, 230)

    def add_actor(self):
        self.textbox_errors.clear()
        if not self.actor.text() or not self.actor_nick.text():
            self.textbox_errors.setText("Введите все поля для эктора")
            return
        for a in acts.actors:
            if a[1] == self.actor_nick.text():
                self.textbox_errors.setText("Ник уже занят")
                return
        for a in acts.actions:
            if a[1] == self.actor_nick.text():
                self.textbox_errors.setText("Ник уже занят")
                return
        acts.actors.append([self.actor.text(), self.actor_nick.text()])
        self.actor_combo.addItem(self.actor_nick.text())
        self.left.addItem(self.actor_nick.text())
        self.right.addItem(self.actor_nick.text())
        self.actor_nick.clear()
        self.actor.clear()

    def add_action(self):
        self.textbox_errors.clear()
        if not self.action.text() or not self.action_nick.text():
            self.textbox_errors.setText("Введите все поля для действия")
            return
        for a in acts.actors:
            if a[1] == self.action_nick.text():
                self.textbox_errors.setText("Ник уже занят")
                return
        for a in acts.actions:
            if a[1] == self.action_nick.text():
                self.textbox_errors.setText("Ник уже занят")
                return
        acts.actions.append([self.action.text(), self.action_nick.text()])
        self.action_combo.addItem(self.action_nick.text())
        self.left.addItem(self.action_nick.text())
        self.right.addItem(self.action_nick.text())
        self.action_nick.clear()
        self.action.clear()

    def edit_link(self):
        self.textbox_errors.clear()
        if not self.left.currentText() or not self.right.currentText():
            self.textbox_errors.setText("Введите все поля для действия")
            return
        for l in acts.linkActs:
            if l.a1 == self.left.currentText() and l.a2 == self.right.currentText() or l.a2 == self.left.currentText() and l.a1 == self.right.currentText():
                l.a1 = self.left.currentText()
                l.a2 = self.right.currentText()
                l.tp = self.link.currentText()
                l.comm = self.comm.text()
                self.comm.clear()
                return
        acts.linkActs.append(LinkActs(self.link.currentText(), self.left.currentText(), self.right.currentText(), self.comm.text()))
        self.comm.clear()

    def delete_actor(self):
        self.textbox_errors.clear()
        if not self.actor_combo.currentText():
            return "Экторов нет"
        i = 0
        for a in acts.actors:
            if a[1] == self.actor_combo.currentText():
                acts.actors.pop(i)
                break
            i += 1
        self.actor_combo.clear()
        self.left.clear()
        self.right.clear()

        for a in acts.actors:
            self.right.addItem(a[1])
            self.left.addItem(a[1])
            self.actor_combo.addItem(a[1])
        for a in acts.actions:
            self.left.addItem(a[1])
            self.right.addItem(a[1])

    def delete_action(self):
        self.textbox_errors.clear()
        if not self.action_combo.currentText():
            return "Действий нет"
        i = 0
        for a in acts.actions:
            if a[1] == self.action_combo.currentText():
                acts.actions.pop(i)
                break
            i += 1
        self.action_combo.clear()
        self.left.clear()
        self.right.clear()

        for a in acts.actions:
            self.left.addItem(a[1])
            self.right.addItem(a[1])
            self.action_combo.addItem(a[1])
        for a in acts.actors:
            self.left.addItem(a[1])
            self.right.addItem(a[1])



    def update(self):
        if len(acts.linkActs) > 0 or len(acts.actors) > 0:
            if self.system.text():
                acts.system_name = self.system.text()
            uml = encoder.encode_acts_diagram(acts).encode(
                'utf-8').hex()
            response = requests.get(f'https://www.plantuml.com/plantuml/png/~h{uml}')
            diagram = QPixmap()
            diagram.loadFromData(response.content)
            w = diagram.width()
            h = diagram.height()
            self.labelLeft.setFixedHeight(h)
            self.labelLeft.setFixedWidth(w)
            self.labelLeft.setPixmap(diagram)
            self.labelLeft.update()
            QApplication.processEvents()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.createMenus()
        self.area = ActsFrame()
        self.setCentralWidget(self.area)

    def createMenus(self):
        self.update = self.menuBar().addAction("&Обновить", self.update)

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addSeparator()

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")

    def update(self):
        self.area.update()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.setGeometry(1000, 1000, 1000, 600)
    ex.setWindowTitle('диаграмма прецедентов')
    ex.show()
    sys.exit(app.exec_())
