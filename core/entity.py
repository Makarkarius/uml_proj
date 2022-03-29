import abc
from typing import List

from core.model import Class, Link, Acts


class Entity(abc.ABC):
    pass


class CDEntity(Entity):
    def __init__(self, classes: List[Class], links: List[Link]):
        self.classes = classes
        self.links = links


class ActsEntity(Entity):
    def __init__(self, acts: Acts):
        self.acts = acts
