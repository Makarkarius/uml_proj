import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, \
    QPushButton, QComboBox, QApplication

from application.menu_controller import MenuController


class Menu(QWidget):
    def __init__(self, controller: MenuController, model=None):
        super().__init__()

        self.controller = controller
        self.model = model

        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.cd = QPushButton("Новая диаграмма классов", self.frame)
        self.cd.clicked.connect(self.show_class_diagram)
        font = QFont()
        font.setPointSize(15)
        self.cd.setFont(font)
        self.cd.resize(400, 40)
        self.cd.move(40, 40)

        self.ad = QPushButton("Новая диаграмма прецедентов", self.frame)
        self.ad.clicked.connect(self.show_acts_diagram)
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
        self.comb.addItems(self.controller.read_names())

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
        self.ad.clicked.connect(self.exit)
        font = QFont()
        font.setPointSize(15)
        self.ad.setFont(font)
        self.ad.resize(400, 40)
        self.ad.move(40, 265)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.frame)

        self.setLayout(hbox)
        self.close()

    def exit(self):
        self.close()
        sys.exit(0)

    def show_class_diagram(self):
        self.hide()
        self.controller.show_class_diagram()

    def show_acts_diagram(self):
        self.hide()
        self.controller.show_acts_diagram()

    def load(self):
        if not self.comb.currentText():
            return
        self.hide()
        self.controller.load(self.comb.currentText())

    def delete(self):
        if not self.comb.currentText():
            return
        self.controller.delete(self.comb.currentText())
        self.comb.clear()
        self.comb.addItems(self.controller.read_names())

    def update(self):
        self.comb.clear()
        data = self.controller.read_names()
        if data is not None:
            self.comb.addItems(data)


app = QApplication(sys.argv)
ctr = MenuController()
menu = Menu(ctr)
menu.setGeometry(1000, 1000, 1000, 600)
menu.setFixedSize(500, 350)
menu.setWindowTitle('uml-редактор')
menu.move(QApplication.desktop().screen().rect().center() - menu.rect().center())
menu.show()
app.exec()
