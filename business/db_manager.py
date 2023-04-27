from PyQt5 import QtSql
from PyQt5.QtSql import QSqlQuery

from core.model import Class


class DBManager:
    def __init__(self, db_name: str):
        self.database = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.database.setDatabaseName(db_name)
        self.database.open()

        self.insert_sql = 'insert into diagram values (?,?,?,?)'
        self.read_names_sql = 'select name from diagram'
        self.is_name_exist_sql = 'select name from diagram'
        self.delete_sql = 'delete from diagram where name=(?)'
        self.load_sql = 'select data, type from diagram where name=(?)'

        self.query = QSqlQuery()
        self.query.prepare('create table if not exists diagram (id integer primary key autoincrement not null, '
                           'name varchar(20), data message_text, type varchar(20))')
        print(Class("", ""))
        if not self.query.exec_():
            raise RuntimeError(self.query.lastError().text())

    def insert_data(self, name, data, data_type):
        self.query = QSqlQuery()
        self.query.prepare(self.insert_sql)
        self.query.addBindValue(None)
        self.query.addBindValue(name)
        self.query.addBindValue(data)
        self.query.addBindValue(data_type)
        if not self.query.exec_():
            raise RuntimeError(self.query.lastError().text())

    def read_names(self) -> list:
        self.query = QSqlQuery()
        self.query.prepare(self.read_names_sql)
        names = []
        if not self.query.exec_():
            raise RuntimeError(self.query.lastError().text())
        else:
            while self.query.next():
                names.append(self.query.value(0))
        return names

    def is_name_exist(self, name) -> bool:
        self.query = QSqlQuery()
        self.query.prepare(self.is_name_exist_sql)
        if not self.query.exec_():
            raise RuntimeError(self.query.lastError().text())
        else:
            while self.query.next():
                if name == self.query.value(0):
                    return True
        return False

    def delete(self, name):
        self.query = QSqlQuery()
        self.query.prepare(self.delete_sql)
        self.query.addBindValue(name)
        if not self.query.exec_():
            raise RuntimeError(self.query.lastError().text())

    def load(self, name):
        self.query = QSqlQuery()
        self.query.prepare(self.load_sql)
        self.query.addBindValue(name)
        if not self.query.exec_():
            raise RuntimeError(self.query.lastError().text())
        else:
            while self.query.next():
                return self.query.value(0), self.query.value(1)
        return None
