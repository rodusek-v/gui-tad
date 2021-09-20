from typing import List

from model.container import Container
from model.item_node import ItemNode


class Player(ItemNode, Container):

    def __init__(
        self,
        name: str = None,
        position: 'Place' = None,
        items: List['Object'] = None
    ) -> None:
        super().__init__()
        self.name = name
        self.position = position
        if items is None:
            items = []
        self.items = items

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def position(self) -> 'Place':
        return self._position

    @position.setter
    def position(self, value: 'Place') -> None:
        self._position = value

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
from model.place import Place
from model.object import Object