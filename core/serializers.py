import codecs
import pickle

from core.entity import Entity


def serialize(entity: Entity):
    return codecs.encode(pickle.dumps(entity), "base64").decode()


def deserialize(data) -> Entity:
    return pickle.loads(codecs.decode(data.encode(), "base64"))
