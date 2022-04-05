from core.entity import ActsEntity
from core.model import Acts
from core.serializers import serialize, deserialize


def test_serialization():
    a = Acts()
    a.system_name = 'abc'
    ac = ActsEntity(a)
    b = deserialize(serialize(ac))
    assert a.system_name == b.acts.system_name