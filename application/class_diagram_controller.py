from PyQt5.QtWidgets import QApplication

from application.util import show_window
from business.db_manager import DBManager
from business.encoder import encode_class_diagram
from business.file_manager import write_data
from business.serializer import serialize
from business.uml_api_manager import request_png, request_svg
from core.entity import CDEntity
from core.model import Class, Link, Field, Method


class ClassDiagramController:
    def __init__(self, model: CDEntity):
        self.model = model
        self.db = DBManager('diagrams.db')

    def show_menu(self):
        import ui.main_window
        ui.main_window.menu.setGeometry(1000, 1000, 1000, 600)
        ui.main_window.menu.setFixedSize(500, 350)
        ui.main_window.menu.setWindowTitle('uml-редактор')
        ui.main_window.menu.move(QApplication.desktop().screen().rect().center() - ui.main_window.menu.rect().center())
        ui.main_window.menu.update()
        ui.main_window.menu.show()

    def export_code(self, dirlist):
        if self.model.classes:
            data = encode_class_diagram(self.model.classes, self.model.links)
            write_data(dirlist, 'txt', 'cd', data, 'w')

    def export_png(self, dirlist):
        if self.model.classes:
            request = encode_class_diagram(self.model.classes, self.model.links).encode('utf-8').hex()
            data = request_png(request)
            write_data(dirlist, 'png', 'cd', data, 'wb')

    def export_svg(self, dirlist):
        if self.model.classes:
            request = encode_class_diagram(self.model.classes, self.model.links).encode('utf-8').hex()
            data = request_svg(request)
            write_data(dirlist, 'svg', 'cd', data, 'wb')

    def save(self) -> str:
        data = serialize(self.model)
        return data

    def update(self) -> bytes:
        data = encode_class_diagram(self.model.classes, self.model.links).encode('utf-8').hex()
        return request_png(data)

    def delete(self, name):
        for i in range(len(self.model.classes)):
            if self.model.classes[i].name == name:
                self.model.classes.pop(i)
                break

    def add_class(self, name, class_type) -> bool:
        cl = Class(name, class_type)
        for c in self.model.classes:
            if c.name == cl.name:
                return True
        self.model.classes.append(cl)
        return False

    def add_link(self, tp, c1, c2, c1_comm, c2_comm, comm) -> bool:
        for link in self.model.links:
            if c2 == link.cl1 and c1 == link.cl2 or c1 == link.cl1 and c2 == link.cl2:
                link.cl1 = c1
                link.cl2 = c2
                link.comm = comm
                link.left = c1_comm
                link.right = c2_comm
                link.tp = tp
                return True
        self.model.links.append(Link(tp, c1, c2, c1_comm, c2_comm, comm))
        return False

    def add_fld(self, ch_class, field_name, field_type, field_mod) -> bool:
        cl = None
        for c in self.model.classes:
            if c.name == ch_class:
                cl = c
                break
        for f in cl.flds:
            if f.name == field_name:
                return True
        cl.flds.append(Field(field_name, field_type, field_mod))
        return False

    def add_mtd(self, ch_class, mt_name, mt_type, mt_mod, mt_params) -> bool:
        cl = None
        for c in self.model.classes:
            if c.name == ch_class:
                cl = c
                break
        for f in cl.mts:
            if f.name == mt_name:
                return True
        cl.mts.append(Method(mt_name, mt_type, mt_mod, mt_params))
        return False

    def delete_method(self, ch_class, del_mt) -> Class:
        cl = self.find_class(ch_class)
        i = 0
        for m in cl.mts:
            if m.name == del_mt:
                cl.mts.pop(i)
                break
            i += 1
        return cl

    def delete_field(self, ch_class, del_field) -> Class:
        cl = self.find_class(ch_class)
        i = 0
        for f in cl.flds:
            if f.name == del_field:
                cl.flds.pop(i)
                break
            i += 1
        return cl

    def find_class(self, ch_class) -> Class:
        cl = None
        for c in self.model.classes:
            if c.name == ch_class:
                cl = c
                break
        return cl

    def is_name_exist(self, name) -> bool:
        exists = False
        try:
            exists = self.db.is_name_exist(name)
        except Exception as e:
            print(str(e))
        return exists

    def insert_data(self, name, data, data_type):
        try:
            self.db.insert_data(name, data, data_type)
        except Exception as e:
            print(str(e))
