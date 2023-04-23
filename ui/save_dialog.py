from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLineEdit


class ClssDialog(QtWidgets.QDialog):
    def __init__(self, controller, data, type, parent=None):
        super(ClssDialog, self).__init__(parent)
        self.controller = controller
        self.data = data
        self.type = type
        self.name = QLineEdit("", self)
        self.name.move(20, 10)
        font = QFont()
        font.setPointSize(8)
        self.name.setPlaceholderText("введите название сохранения")
        self.name.resize(210, 20)
        self.name.setFont(font)

        self.textbox_errors = QLineEdit("", self)
        self.textbox_errors.setReadOnly(True)
        self.textbox_errors.move(20, 40)
        self.textbox_errors.setFrame(False)
        font = QFont()
        font.setPointSize(10)
        self.textbox_errors.setFont(font)
        self.textbox_errors.setMinimumSize(15, 15)
        self.textbox_errors.setMaximumSize(300, 20)
        self.textbox_errors.resize(300, 20)

        self.textbox_errors.setStyleSheet('background-color: #f0f0f0; border: none; color: red;')
        self.ok_btn = QtWidgets.QPushButton(self)
        self.ok_btn.clicked.connect(self.save)
        self.ok_btn.move(20, 70)
        self.close_btn = QtWidgets.QPushButton(self)
        self.close_btn.clicked.connect(self.close)
        self.close_btn.move(155, 70)
        self.ok_btn.setText("Сохранить")
        self.close_btn.setText("Закрыть")

    def save(self):
        self.textbox_errors.clear()
        if not self.name.text():
            self.textbox_errors.setText("Введите название сохранения")
            return
        if self.controller.is_name_exist(self.name.text()):
            self.textbox_errors.setText("Такое название уже существует")
            return
        self.controller.insert_data(self.name.text(), self.data, self.type)
        self.close()

