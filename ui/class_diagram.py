import sys
from typing import List

import requests as requests
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from core.encoder import encode_class_diagram
from core.model import Class, Link, Field, Method

classes = [Class('123', 'class')]
cl_links: List[Link] = []
links = ['агрегация', 'композиция', 'наследование', 'ассоциация', 'связь', 'без связи']
modificators = ['public', 'package private', 'protected', 'private', 'отсутсвует']
cl_types = ['class', 'enum', 'interface', 'entity', 'abstract class']


class CDFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.diagram = QPixmap('')

        self.topRight = QFrame()
        self.topRight.setFrameShape(QFrame.StyledPanel)
        self.botRight = QFrame()
        self.botRight.setFrameShape(QFrame.StyledPanel)


        self.write_class = QLineEdit(self.botRight)
        self.write_class.setPlaceholderText('имя класса')
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
        splitter1.setSizes([20, 13])

        splitter2 = QSplitter(Qt.Horizontal)

        splitter2.addWidget(self.leftFrame)
        splitter2.addWidget(splitter1)
        splitter2.setSizes([30, 14])

        hbox = QHBoxLayout(self)
        hbox.addWidget(splitter2)

        self.textbox_classes_errors = QLineEdit("", self.botRight)
        self.textbox_classes_errors.setReadOnly(True)
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
        self.create_attr_for_mts()

    def create_btns_for_classes(self):

        self.del_class_btn = QPushButton("удалить класс", self.botRight)
        self.del_class_btn.clicked.connect(self.delete)
        self.del_class_btn.resize(100, 20)
        self.del_class_btn.move(170, 0)

        self.add_class_btn = QPushButton("добавить класс", self.botRight)
        self.add_class_btn.move(170, 20)
        self.add_class_btn.resize(100, 20)
        self.add_class_btn.clicked.connect(self.add_class)

    def create_attr_for_mts(self):
        ql = QLabel("Редактируемый класс", self.topRight)
        ql.move(10, 0)

        self.ch_class = QComboBox(self.topRight)
        self.ch_class.resize(100, 20)
        self.ch_class.move(10, 25)
        for c in classes:
            self.ch_class.addItem(c.name)

        fl = QLabel("Добавить поле", self.topRight)
        fl.move(10, 60)
        self.field_name = QLineEdit(self.topRight)
        self.field_name.setPlaceholderText("имя поля")
        self.field_type = QLineEdit(self.topRight)
        self.field_type.setPlaceholderText("тип поля")
        self.field_mod = QComboBox(self.topRight)
        self.field_mod.addItems(modificators)
        self.field_name.move(0, 85)
        self.field_name.resize(100, 20)
        self.field_type.move(105, 85)
        self.field_type.resize(100, 20)
        self.field_mod.move(210, 85)
        self.field_mod.resize(100, 20)
        self.add_field = QPushButton('добавить поле', self.topRight)
        self.add_field.move(112, 110)
        self.add_field.clicked.connect(self.add_fld)

        ml = QLabel("Добавить метод", self.topRight)
        ml.move(10, 140)
        self.mt_name = QLineEdit(self.topRight)
        self.mt_name.setPlaceholderText("имя метода")
        self.mt_type = QLineEdit(self.topRight)
        self.mt_type.setPlaceholderText("возвр. значение")
        self.mt_mod = QComboBox(self.topRight)
        self.mt_mod.addItems(modificators)
        self.mt_name.move(0, 165)
        self.mt_name.resize(100, 20)
        self.mt_type.move(105, 165)
        self.mt_type.resize(100, 20)
        self.mt_mod.move(210, 165)
        self.mt_mod.resize(100, 20)
        self.mt_params = QLineEdit(self.topRight)
        self.mt_params.resize(150, 20)
        self.mt_params.move(0, 190)
        self.mt_params.setPlaceholderText('параметры метода')
        self.add_mt = QPushButton('добавить метод', self.topRight)
        self.add_mt.clicked.connect(self.add_mtd)
        self.add_mt.move(110, 215)

        self.del_field = QComboBox(self.topRight)
        self.del_mt = QComboBox(self.topRight)
        if self.ch_class.currentText():
            cl = None
            for c in classes:
                if c.name == self.ch_class.currentText():
                    cl = c
                    break
            for m in cl.mts:
                self.del_mt.addItem(m.name)
            for f in cl.flds:
                self.del_mt.addItem(f.name)
        self.del_field.resize(100, 20)
        self.del_mt.resize(100, 20)
        self.del_field.move(10, 255)
        self.del_mt.move(115, 255)
        self.del_field.resize(100, 20)
        self.del_mt.resize(100, 20)

        self.del_field_b = QPushButton('удалить поле', self.topRight)
        self.del_field_b.clicked.connect(self.d_f)
        self.del_mt_b = QPushButton('удалить метод', self.topRight)
        self.del_mt_b.clicked.connect(self.d_m)
        self.del_field_b.resize(100, 20)
        self.del_mt_b.resize(100, 20)
        self.del_field_b.move(10, 280)
        self.del_mt_b.move(115, 280)
        self.del_field_b.resize(100, 20)
        self.del_mt_b.resize(100, 20)

        self.textbox_attr_errors = QLineEdit("", self.topRight)
        self.textbox_attr_errors.setReadOnly(True)
        self.textbox_attr_errors.move(10, 180)
        self.textbox_attr_errors.setFrame(False)
        font = QFont()
        font.setPointSize(11)
        self.textbox_attr_errors.setFont(font)
        self.textbox_attr_errors.resize(300, 20)
        self.textbox_attr_errors.setStyleSheet('background-color: #f0f0f0; border: none; color: red;')
        self.textbox_attr_errors.move(10, 310)

        self.ch_class.currentTextChanged.connect(self.change)




    def create_combos_for_classes(self):
        ql = QLabel("связи классов", self.botRight)
        ql.move(90, 55)

        self.classes_type = QComboBox(self.botRight)
        self.classes_type.addItems(cl_types)
        self.classes_type.resize(66, 20)
        self.classes_type.move(102, 20)

        self.classes_combo = QComboBox(self.botRight)
        for c in classes:
            self.classes_combo.addItem(c.name)
        self.classes_combo.resize(100, 20)

        self.c1_combo = QComboBox(self.botRight)
        for c in classes:
            self.c1_combo.addItem(c.name)
        self.c1_combo.move(0, 70)
        self.c1_combo.resize(80, 20)
        self.comment_c1 = QLineEdit(self.botRight)
        self.comment_c1.setPlaceholderText('комм')
        self.comment_c1.resize(80, 20)
        self.comment_c1.move(0, 95)

        self.link_combo = QComboBox(self.botRight)
        self.link_combo.addItems(links)
        self.link_combo.move(85, 70)
        self.link_combo.resize(80, 20)
        self.comment_link = QLineEdit(self.botRight)
        self.comment_link.setPlaceholderText('комм')
        self.comment_link.resize(80, 20)
        self.comment_link.move(85, 95)
        self.btn_link = QPushButton("добавить изменения", self.botRight)
        self.btn_link.clicked.connect(self.add_link)
        self.btn_link.resize(120, 20)
        self.btn_link.move(65, 120)

        self.c2_combo = QComboBox(self.botRight)
        for c in classes:
            self.c2_combo.addItem(c.name)
        self.c2_combo.move(170, 70)
        self.c2_combo.resize(80, 20)
        self.comment_c2 = QLineEdit(self.botRight)
        self.comment_c2.setPlaceholderText('комм')
        self.comment_c2.resize(80, 20)
        self.comment_c2.move(170, 95)

    def delete(self):
        self.textbox_classes_errors.clear()
        if not classes:
            return
        for i in range(len(classes)):
            if classes[i].name == self.classes_combo.currentText():
                classes.pop(i)
                break
        self.classes_combo.clear()
        self.c1_combo.clear()
        self.c2_combo.clear()
        self.ch_class.clear()
        for c in classes:
            self.classes_combo.addItem(c.name)
            self.c1_combo.addItem(c.name)
            self.c2_combo.addItem(c.name)
            self.ch_class.addItem(c.name)

    def add_class(self):
        self.textbox_classes_errors.clear()
        if not self.write_class.text():
            return
        cl = Class(self.write_class.text(), self.classes_type.currentText())
        for c in classes:
            if c.name == cl.name:
                self.textbox_classes_errors.setText("Такой класс уже существует")
                return
        classes.append(cl)
        self.classes_combo.clear()
        self.write_class.clear()
        self.c1_combo.clear()
        self.c2_combo.clear()
        self.ch_class.clear()
        for c in classes:
            self.classes_combo.addItem(c.name)
            self.c1_combo.addItem(c.name)
            self.c2_combo.addItem(c.name)
            self.ch_class.addItem(c.name)

    def add_link(self):
        self.textbox_classes_errors.clear()
        c1 = self.c1_combo.currentText()
        c2 = self.c2_combo.currentText()
        tp = self.link_combo.currentText()
        c1_comm = self.comment_c1.text()
        c2_comm = self.comment_c2.text()
        comm = self.comment_link.text()

        if c1 == '' or c2 == '':
            self.textbox_classes_errors.setText("введите все классы")
            return
        for l in cl_links:
            if c2 == l.cl1 and c1 == l.cl2 or c1 == l.cl1 and c2 == l.cl2:
                l.cl1 = c1
                l.cl2 = c2
                l.comm = comm
                l.left = c1_comm
                l.right = c2_comm
                l.tp = tp
                return
        cl_links.append(Link(tp, c1, c2, c1_comm, c2_comm, comm))
        self.comment_c1.clear()
        self.comment_c2.clear()
        self.comment_link.clear()

    def add_fld(self):
        self.textbox_attr_errors.clear()
        if not self.ch_class.currentText():
            self.textbox_attr_errors.setText('Добавьте класс')
            return
        if not self.field_name.text():
            self.textbox_attr_errors.setText('Введите имя поля')
            return
        cl = None
        for c in classes:
            if c.name == self.ch_class.currentText():
                cl = c
                break
        for f in cl.flds:
            if f.name == self.field_name.text():
                self.textbox_attr_errors.setText('Поле с таким именем уже есть')
                return
        cl.flds.append(Field(self.field_name.text(), self.field_type.text(), self.field_mod.currentText()))
        self.del_field.addItem(self.field_name.text())
        self.field_name.setText('')
        self.field_type.setText('')

    def add_mtd(self):
        self.textbox_attr_errors.clear()
        if not self.ch_class.currentText():
            self.textbox_attr_errors.setText('Добавьте класс')
            return
        if not self.mt_name.text():
            self.textbox_attr_errors.setText('Введите имя метода')
            return
        cl = None
        for c in classes:
            if c.name == self.ch_class.currentText():
                cl = c
                break
        for f in cl.mts:
            if f.name == self.mt_name.text():
                self.textbox_attr_errors.setText('Метод с таким именем уже есть')
                return
        cl.mts.append(Method(self.mt_name.text(), self.mt_type.text(),
                             self.mt_mod.currentText(), self.mt_params.text()))
        self.del_mt.addItem(self.mt_name.text())
        self.mt_name.setText('')
        self.mt_type.setText('')
        self.mt_params.setText('')

    def change(self):
        self.del_mt.clear()
        self.del_field.clear()
        if self.ch_class.currentText():
            cl = None
            for c in classes:
                if c.name == self.ch_class.currentText():
                    cl = c
                    break
            for m in cl.mts:
                self.del_mt.addItem(m.name)
            for f in cl.flds:
                self.del_mt.addItem(f.name)

    def d_m(self):
        if not self.del_mt.currentText():
            return
        cl = None
        for c in classes:
            if c.name == self.ch_class.currentText():
                cl = c
                break
        i = 0
        for m in cl.mts:
            if m.name == self.del_mt.currentText():
                cl.mts.pop(i)
                break
            i += 1
        self.del_mt.clear()
        for m in cl.mts:
            self.del_mt.addItem(m.name)

    def d_f(self):
        if not self.del_field.currentText():
            return
        cl = None
        for c in classes:
            if c.name == self.ch_class.currentText():
                cl = c
                break
        i = 0
        for f in cl.flds:
            if f.name == self.del_field.currentText():
                cl.flds.pop(i)
                break
            i += 1
        self.del_field.clear()
        for f in cl.flds:
            self.del_field.addItem(f.name)


    def update(self):
        if classes:
            data = encode_class_diagram(classes, cl_links).encode(
                'utf-8').hex()
            response = requests.get(f'https://www.plantuml.com/plantuml/png/~h{data}')
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
    ex.setWindowTitle('диаграмма классов')
    ex.show()
    sys.exit(app.exec_())
