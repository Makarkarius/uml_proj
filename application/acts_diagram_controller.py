from PyQt5.QtWidgets import QApplication

from business.db_manager import DBManager
from business.encoder import encode_acts_diagram
from business.file_manager import write_data
from business.serializer import serialize
from business.uml_api_manager import request_png, request_svg
from core.entity import ActsEntity
from core.model import LinkActs


class ActsDiagramController:
    def __init__(self, model: ActsEntity):
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
        if self.model.acts:
            data = encode_acts_diagram(self.model.acts)
            write_data(dirlist, 'txt', 'ac', data, 'w')

    def export_png(self, dirlist):
        if self.model.acts:
            request = encode_acts_diagram(self.model.acts).encode('utf-8').hex()
            data = request_png(request)
            write_data(dirlist, 'png', 'ac', data, 'wb')

    def export_svg(self, dirlist):
        if self.model.acts:
            request = encode_acts_diagram(self.model.acts).encode('utf-8').hex()
            data = request_svg(request)
            write_data(dirlist, 'svg', 'ac', data, 'wb')

    def save(self) -> str:
        data = serialize(self.model)
        return data

    def update(self) -> bytes:
        data = encode_acts_diagram(self.model.acts).encode('utf-8').hex()
        return request_png(data)

    def add_actor(self, actor_nick, actor) -> bool:
        if self.nick_exists(actor_nick):
            return True
        self.model.acts.actors.append([actor, actor_nick])
        return False

    def add_action(self, action_nick, action) -> bool:
        if self.nick_exists(action_nick):
            return True
        self.model.acts.actions.append([action, action_nick])
        return False

    def nick_exists(self, nick) -> bool:
        for a in self.model.acts.actors:
            if a[1] == nick:
                return True
        for a in self.model.acts.actions:
            if a[1] == nick:
                return True
        return False

    def edit_link(self, left, right, link, comm):
        for l in self.model.acts.linkActs:
            if l.a1 == left and l.a2 == right or l.a2 == left \
                    and l.a1 == right:
                l.a1 = left
                l.a2 = right
                l.tp = link
                l.comm = comm
                return
        self.model.acts.linkActs.append(LinkActs(link, left, right, comm))

    def delete_actor(self, actor_combo):
        i = 0
        for a in self.model.acts.actors:
            if a[1] == actor_combo:
                self.model.acts.actors.pop(i)
                break
            i += 1

    def delete_action(self, action_combo):
        i = 0
        for a in self.model.acts.actions:
            if a[1] == action_combo:
                self.model.acts.actions.pop(i)
                break
            i += 1

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
