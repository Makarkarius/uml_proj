import sys

import requests as requests
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

classes = []


class Example(QWidget):
    def __init__(self):
        super().__init__()
        a = '@startuml\nBob -> Alice : hello\nBob -> Alice : hello\nBob -> Alice : hello\n@enduml'.encode('utf-8').hex()
        response = requests.get(f'https://www.plantuml.com/plantuml/png/~h{a}')

        self.diagram = QPixmap()
        self.diagram.loadFromData(response.content)

        self.topRight = QFrame()
        self.topRight.setFrameShape(QFrame.StyledPanel)
        self.botRight = QFrame()
        self.botRight.setFrameShape(QFrame.StyledPanel)


        self.write_class = QLineEdit(self.botRight)
        self.write_class.move(0, 20)


        self.combo = QComboBox(self.botRight)
        self.combo.addItems(classes)
        self.combo.activated[str].connect(self.onActivated)

        leftFrame = QFrame()
        leftFrame.setFrameShape(QFrame.StyledPanel)

        labelLeft = QLabel(" labelLeft", leftFrame)
        labelLeft.setPixmap(self.diagram)
        labelLeft.setAlignment(Qt.AlignCenter)

        splitter1 = QSplitter(Qt.Vertical)


        splitter1.addWidget(self.topRight)
        splitter1.addWidget(self.botRight)

        splitter2 = QSplitter(Qt.Horizontal)

        splitter2.addWidget(leftFrame)
        splitter2.addWidget(splitter1)
        splitter2.setSizes([30, 10])

        hbox = QHBoxLayout(self)
        hbox.addWidget(splitter2)
        self.setLayout(hbox)
        self.create_btns()

    def create_btns(self):

        del_class_btn = QPushButton("del", self.botRight)
        del_class_btn.clicked.connect(self.delete)
        del_class_btn.move(150, 0)

        add_class_btn = QPushButton("add", self.botRight)
        add_class_btn.move(150, 20)
        add_class_btn.clicked.connect(self.add)

    def onActivated(self, text):
        a = text
        a += ""

    def delete(self):
        if not classes:
            return
        classes.pop(classes.index(self.combo.currentText()))
        self.combo.clear()
        self.combo.addItems(classes)

    def add(self):
        if not self.write_class.text():
            return
        classes.append(self.write_class.text())
        self.combo.clear()
        self.combo.addItems(classes)

    def update(self):
        print(1)



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.createMenus()
        self.area = Example()
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
    ex.setGeometry(800, 800, 800, 600)
    ex.setWindowTitle('QSplitter demo')
    ex.show()
    sys.exit(app.exec_())
