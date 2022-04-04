from PyQt5 import QtSql
from PyQt5.QtSql import QSqlQuery

from core.model import Class

database = QtSql.QSqlDatabase.addDatabase('QSQLITE')
database.setDatabaseName('diagrams.db')
database.open()

query = QSqlQuery()
query.prepare('create table diagram (id integer primary key autoincrement not null, '
              'name varchar(20), data message_text, type varchar(20))')
print(Class("", ""))
if not query.exec_():
    query.lastError()


def insert_data(name, data, type):
    insert_sql = 'insert into diagram values (?,?,?,?)'
    query.prepare(insert_sql)
    query.addBindValue(None)
    query.addBindValue(name)
    query.addBindValue(data)
    query.addBindValue(type)
    if not query.exec_():
        print(query.lastError())


def read_names():
    query.prepare('select name from diagram')
    names = []
    if not query.exec_():
        query.lastError()
    else:
        while query.next():
            names.append(query.value(0))
    return names


def is_name_exist(name):
    query.prepare('select name from diagram')
    if not query.exec_():
        query.lastError()
    else:
        while query.next():
            if name == query.value(0):
                return True
    return False


def delete(name):
    query.prepare('delete from diagram where name=(?)')
    query.addBindValue(name)
    if not query.exec_():
        print(query.lastError())


def load(name):
    query.prepare('select data, type from diagram where name=(?)')
    query.addBindValue(name)
    if not query.exec_():
        query.lastError()
    else:
        while query.next():
            return query.value(0), query.value(1)
    return None

