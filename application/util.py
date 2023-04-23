from PyQt5.QtWidgets import QApplication, QWidget


def show_window(window: QWidget, title: str):
    window.setGeometry(1000, 1000, 1000, 600)
    window.setWindowTitle(title)
    window.move(QApplication.desktop().screen().rect().center() - window.rect().center())
    window.show()
