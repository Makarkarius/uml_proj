from PyQt5 import QtSql
from PyQt5.QtSql import QSqlQuery

database = QtSql.QSqlDatabase.addDatabase('QSQLITE')
database.setDatabaseName('test.db')
database.open()

query = QSqlQuery()
query.prepare('create table student (id int primary key, name message_text ,age int)')
if not query.exec_():
    query.lastError()
else:
    print('create a table')

insert_sql = 'insert into student values (?,?,?)'
query.prepare(insert_sql)
query.addBindValue(4)
query.addBindValue('test3')
query.addBindValue(1)
if not query.exec_():
    print(query.lastError())
else:
    print('inserted')


query.prepare('select id,name,age from student')
if not query.exec_():
    query.lastError()
else:
    while query.next():
        id = query.value(0)
        name = query.value(1)
        age = query.value(2)
        print(id,name,age)