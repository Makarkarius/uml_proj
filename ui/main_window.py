import sys

import requests
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFrame, QSplitter, QLabel, QLineEdit, QHBoxLayout, \
    QPushButton, QComboBox

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

        self.open = QPushButton("Загрузить", self.frame)
        font = QFont()
        font.setPointSize(15)
        self.open.setFont(font)
        self.open.resize(200, 40)
        self.open.move(40, 205)

        self.clos = QPushButton("Удалить", self.frame)
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
        ex = class_diagram.MainWindow()
        ex.setGeometry(1000, 1000, 1000, 600)
        ex.setWindowTitle('диаграмма классов')
        ex.move(QApplication.desktop().screen().rect().center() - ex.rect().center())
        ex.show()

    def ac(self):
        global ex
        self.close()
        ex = acts_diagram.MainWindow()
        ex.setGeometry(1000, 1000, 1000, 600)
        ex.setWindowTitle('диаграмма прецедентов')
        ex.move(QApplication.desktop().screen().rect().center() - ex.rect().center())
        ex.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.setGeometry(1000, 1000, 1000, 600)
    ex.setFixedSize(500, 350)
    ex.setWindowTitle('меню')
    ex.move(QApplication.desktop().screen().rect().center() - ex.rect().center())
    ex.show()
    sys.exit(app.exec_())
