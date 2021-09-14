from typing import List
from PyQt6.QtCore import QObject

from model.item_node import ItemNode

class Player(QObject, ItemNode):

    def __init__(
        self,
        name=None,
        position=None,
        items=list()
    ) -> None:
        super().__init__()
        self.name = name
        self.position = position
        self.items = items

    def get_objects(self) -> List['Object']:
        return self.items

    def add_object(self, object: 'Object') -> None:
        object.container = self
        self.items.append(object)

    def remove_object(self, object: 'Object') -> None:
        try:
            self.items.remove(object)
            del object.container
        except ValueError:
            pass

from model.object import Object