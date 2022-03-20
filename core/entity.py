from typing import List

from core.model import Class, Link


class CDEntity:
    def __init__(self, classes: List[Class], links: List[Link]):
        self.classes = classes
        self.links = links
