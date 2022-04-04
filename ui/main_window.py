import sys

import requests
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFrame, QSplitter, QLabel, QLineEdit, QHBoxLayout, \
    QPushButton, QComboBox

from core import db_manager
from core.db_manager import insert_data, read_names, delete, load
from core.model import Class, Acts
from core.serializers import deserialize
from ui import acts_diagram


class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.cd = QPushButton("Новая диаграмма классов", self.frame)
        self.cd.clicked.connect(self.cl)
        font = QFont()
        font.setPointSize(15)
        self.cd.setFont(font)
        self.cd.resize(400, 40)
        self.cd.move(40, 40)

        self.ad = QPushButton("Новая диаграмма прецедентов", self.frame)
        self.ad.clicked.connect(self.ac)
        font = QFont()
        font.setPointSize(15)
        self.ad.setFont(font)
        self.ad.resize(400, 40)
        self.ad.move(40, 100)

        self.comb = QComboBox(self.frame)
        font = QFont()
        font.setPointSize(15)
        self.comb.setFont(font)
        self.comb.resize(400, 40)
        self.comb.move(40, 160)
        self.comb.addItems(read_names())

        self.open = QPushButton("Загрузить", self.frame)
        self.open.clicked.connect(self.load)
        font = QFont()
        font.setPointSize(15)
        self.open.setFont(font)
        self.open.resize(200, 40)
        self.open.move(40, 205)

        self.clos = QPushButton("Удалить", self.frame)
        self.clos.clicked.connect(self.delete)
        font = QFont()
        font.setPointSize(15)
        self.clos.setFont(font)
        self.clos.resize(200, 40)
        self.clos.move(240, 205)

        self.ad = QPushButton("Выход", self.frame)
        self.ad.clicked.connect(self.close)
        font = QFont()
        font.setPointSize(15)
        self.ad.setFont(font)
        self.ad.resize(400, 40)
        self.ad.move(40, 265)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.frame)

        self.setLayout(hbox)
        self.close()

    def cl(self):
        global ex
        self.close()
        from ui import class_diagram
        class_diagram.classes = []
        class_diagram.cl_links = []
        ex = class_diagram.MainWindow()
        ex.setGeometry(1000, 1000, 1000, 600)
        ex.setWindowTitle('диаграмма классов')
        ex.move(QApplication.desktop().screen().rect().center() - ex.rect().center())
        ex.show()

    def ac(self):
        global ex
        self.close()
        acts_diagram.acts = Acts()
        ex = acts_diagram.MainWindow()
        ex.setGeometry(1000, 1000, 1000, 600)
        ex.setWindowTitle('диаграмма прецедентов')
        ex.move(QApplication.desktop().screen().rect().center() - ex.rect().center())
        ex.show()

    def load(self):
        if not self.comb.currentText():
            return
        self.close()
        ans = load(self.comb.currentText())
        data = deserialize(ans[0])
        global ex
        if ans[1] == 'cd':
            from ui import class_diagram
            class_diagram.classes = data.classes
            class_diagram.cl_links = data.links
            ex = class_diagram.MainWindow()
            ex.setGeometry(1000, 1000, 1000, 600)
            ex.setWindowTitle('диаграмма классов')
            ex.move(QApplication.desktop().screen().rect().center() - ex.rect().center())
            ex.show()
        elif ans[1] == 'ac':
            acts_diagram.acts = data.acts
            ex = acts_diagram.MainWindow()
            ex.setGeometry(1000, 1000, 1000, 600)
            ex.setWindowTitle('диаграмма прецедентов')
            ex.move(QApplication.desktop().screen().rect().center() - ex.rect().center())
            ex.show()

    def delete(self):
        if not self.comb.currentText():
            return
        delete(self.comb.currentText())
        self.comb.clear()
        self.comb.addItems(read_names())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.setGeometry(1000, 1000, 1000, 600)
    ex.setFixedSize(500, 350)
    ex.setWindowTitle('uml-редактор')
    ex.move(QApplication.desktop().screen().rect().center() - ex.rect().center())
    ex.show()
    sys.exit(app.exec_())
