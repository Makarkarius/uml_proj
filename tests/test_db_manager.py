from business.db_manager import DBManager
from business.encoder import encode_acts_diagram, encode_class_diagram
from core.model import Class, Field, Acts


def test_insert_load():
    db = DBManager('test')
    name = 'test_name'
    data = 'asdasdasd'
    data_type = 'text'
    try:
        db.insert_data(name, data, data_type)
    except Exception as exc:
        assert False, f"'insert_data' raised an exception {exc}"
    try:
        ans = db.load(name)
        assert ans[1] == data_type
        assert ans[0] == data
    except Exception as exc:
        assert False, f"'load' raised an exception {exc}"
