from business.encoder import encode_acts_diagram, encode_class_diagram
from core.model import Class, Field, Acts

str = "@startuml\nclass ааа {\n+ 123 asdas\n}\n@enduml"


def test_cd_encoder():
    cl = [Class('ааа', 'class')]
    cl[0].flds.append(Field('asdas', '123', 'public'))
    assert encode_class_diagram(cl, []) == str


def test_ac_encoder():
    acts = Acts()
    acts.actors.append(('123', '123'))
    acts.system_name = '123'
    assert encode_acts_diagram(acts) == '@startuml\nrectangle 123{\n}\n:123: as 123\n@enduml'
