import sys

import requests as requests
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

classes = [('a', 'n')]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        a = '@startuml\nBob -> Alice : hello\nBob -> Alice : hello\nBob -> Alice : hello\n@enduml'.encode('utf-8').hex()
        response = requests.get(f'https://www.plantuml.com/plantuml/png/~h{a}')

        pixmap = QPixmap()
        pixmap.loadFromData(response.content)

        topRight = QFrame()
        topRight.setFrameShape(QFrame.StyledPanel)
        botRight = QFrame()
        botRight.setFrameShape(QFrame.StyledPanel)
        labelTopRight = QLabel(" labelTopRight", topRight)
        del_class = QPushButton("del", botRight)
        self.write_class = QLineEdit(botRight)
        self.write_class.move(0, 20)
        add_class = QPushButton("add", botRight)
        add_class.move(150, 20)
        del_class.clicked.connect(self.delete)
        add_class.clicked.connect(self.add)
        del_class.move(150, 0)
        self.combo = QComboBox(botRight)
        self.combo.addItems(classes)
        self.combo.activated[str].connect(self.onActivated)

        leftFrame = QFrame()
        leftFrame.setFrameShape(QFrame.StyledPanel)
        labelLeft = QLabel(" labelLeft", leftFrame)
        labelLeft.setPixmap(pixmap)
        labelLeft.setAlignment(Qt.AlignCenter)

        splitter1 = QSplitter(Qt.Vertical)


        splitter1.addWidget(topRight)
        splitter1.addWidget(botRight)

        splitter2 = QSplitter(Qt.Horizontal)

        splitter2.addWidget(leftFrame)
        splitter2.addWidget(splitter1)
        splitter2.setSizes([30, 10])

        hbox = QHBoxLayout(self)
        hbox.addWidget(splitter2)
        self.setLayout(hbox)

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


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.createMenus()
        self.area = Example()
        self.setCentralWidget(self.area)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addSeparator()

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.setGeometry(800, 800, 800, 600)
    ex.setWindowTitle('QSplitter demo')
    ex.show()
    sys.exit(app.exec_())
