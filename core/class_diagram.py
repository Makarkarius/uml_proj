import sys

import requests as requests
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from core.model import Class

classes = []
cl_types = ['class', 'enum', 'interface']


class CDFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.diagram = QPixmap('')

        self.topRight = QFrame()
        self.topRight.setFrameShape(QFrame.StyledPanel)
        self.botRight = QFrame()
        self.botRight.setFrameShape(QFrame.StyledPanel)


        self.write_class = QLineEdit(self.botRight)
        self.write_class.resize(100, 20)
        self.write_class.move(0, 20)

        self.leftFrame = QFrame()
        self.leftFrame.setFrameShape(QFrame.StyledPanel)

        self.labelLeft = QLabel(" labelLeft", self.leftFrame)
        self.labelLeft.setAlignment(Qt.AlignCenter)
        self.labelLeft.setPixmap(self.diagram)



        splitter1 = QSplitter(Qt.Vertical)


        splitter1.addWidget(self.topRight)
        splitter1.addWidget(self.botRight)

        splitter2 = QSplitter(Qt.Horizontal)

        splitter2.addWidget(self.leftFrame)
        splitter2.addWidget(splitter1)
        splitter2.setSizes([30, 14])

        hbox = QHBoxLayout(self)
        hbox.addWidget(splitter2)

        self.textbox_classes_errors = QLineEdit("sadfsdfffffffffffffffffffffffffffff", self.botRight)
        self.textbox_classes_errors.readOnly = True
        self.textbox_classes_errors.move(10, 180)
        self.textbox_classes_errors.setFrame(False)
        font = QFont()
        font.setPointSize(11)
        self.textbox_classes_errors.setFont(font)



        self.textbox_classes_errors.setMinimumSize(15, 15)
        self.textbox_classes_errors.setMaximumSize(300, 20)
        self.textbox_classes_errors.resize(300, 20)

        self.textbox_classes_errors.setStyleSheet('background-color: #f0f0f0; border: none; color: red;')



        self.setLayout(hbox)
        self.create_btns_for_classes()
        self.create_combos_for_classes()
        self.create_combos_for_mts()

    def create_btns_for_classes(self):

        self.del_class_btn = QPushButton("удалить класс", self.botRight)
        self.del_class_btn.clicked.connect(self.delete)
        self.del_class_btn.resize(100, 20)
        self.del_class_btn.move(170, 0)

        self.add_class_btn = QPushButton("добавить класс", self.botRight)
        self.add_class_btn.move(170, 20)
        self.add_class_btn.resize(100, 20)
        self.add_class_btn.clicked.connect(self.add)

    def create_combos_for_mts(self):
        ql = QLabel("Редактируемый класс", self.topRight)
        ql.move(10, 0)
        self.ch_class = QComboBox(self.topRight)
        self.ch_class.resize(100, 20)
        self.ch_class.move(20, 25)

    def create_combos_for_classes(self):
        ql = QLabel("связи классов", self.botRight)
        ql.move(80, 55)

        self.classes_type = QComboBox(self.botRight)
        self.classes_type.addItems(cl_types)
        self.classes_type.resize(66, 20)
        self.classes_type.move(102, 20)
        self.classes_type.activated[str].connect(self.onActivated)

        self.classes_combo = QComboBox(self.botRight)
        self.classes_combo.addItems(classes)
        self.classes_combo.resize(100, 20)
        self.classes_combo.activated[str].connect(self.onActivated)

        self.c1_combo = QComboBox(self.botRight)
        self.c1_combo.addItems(classes)
        self.c1_combo.move(0, 70)
        self.c1_combo.resize(80, 20)
        self.c1_combo.activated[str].connect(self.onActivated)
        self.comment_c1 = QLineEdit(self.botRight)
        self.comment_c1.resize(80, 20)
        self.comment_c1.move(0, 95)

        self.link_combo = QComboBox(self.botRight)
        self.link_combo.addItems(classes)
        self.link_combo.move(85, 70)
        self.link_combo.resize(60, 20)
        self.link_combo.activated[str].connect(self.onActivated)
        self.comment_link = QLineEdit(self.botRight)
        self.comment_link.resize(60, 20)
        self.comment_link.move(85, 95)
        self.btn_link = QPushButton("добавить изменения", self.botRight)
        self.btn_link.resize(120, 20)
        self.btn_link.move(55, 120)

        self.c2_combo = QComboBox(self.botRight)
        self.c2_combo.addItems(classes)
        self.c2_combo.move(150, 70)
        self.c2_combo.resize(80, 20)
        self.c2_combo.activated[str].connect(self.onActivated)
        self.comment_c2 = QLineEdit(self.botRight)
        self.comment_c2.resize(80, 20)
        self.comment_c2.move(150, 95)

    def onActivated(self, text):
        a = text
        a += ""

    def delete(self):
        self.textbox_classes_errors.clear()
        if not classes:
            return
        for i in range(len(classes)):
            if classes[i].name == self.classes_combo.currentText():
                classes.pop(i)
                break
        self.classes_combo.clear()
        for c in classes:
            self.classes_combo.addItem(c.name)

    def add(self):
        self.textbox_classes_errors.clear()
        if not self.write_class.text():
            return
        cl = Class(self.write_class.text())
        classes.append(cl)
        self.classes_combo.clear()
        self.write_class.clear()
        for c in classes:
            self.classes_combo.addItem(c.name)

    def update(self):
        if not classes:
            a = '@startuml\nclass Class11\nClass11->Class12\n@enduml'.encode(
                'utf-8').hex()
            response = requests.get(f'https://www.plantuml.com/plantuml/png/~h{a}')
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
        self.area = CDFrame()
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
    ex.setWindowTitle('class diagramm')
    ex.show()
    sys.exit(app.exec_())
