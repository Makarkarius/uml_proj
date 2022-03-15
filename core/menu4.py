import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Model Example'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 240
        self.initUI()

    def initUI(self):
        self.model = QStandardItemModel(0, 3, None)

        self.cb = QComboBox()
        self.model.insertRow(0)
        self.model.setData(self.model.index(0, 0), 'C++')
        self.model.insertRow(1)
        self.model.setData(self.model.index(1, 0), 'Java')
        self.cb.setModel(self.model)

        but = QPushButton('Delete')
        but.clicked.connect(self.on_click)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.cb)
        mainLayout.addWidget(but)

        self.setLayout(mainLayout)

        self.show()

    def on_click(self):
        # print(dir(self.model))
        self.model.removeRow(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())