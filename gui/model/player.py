from typing import List

from PyQt6.QtGui import QIcon

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
    def q_icon(self) -> QIcon:
        if self._q_icon is None:
            icon = QIcon()
            icon.addFile("icons/player.png", mode=QIcon.Mode.Active)
            icon.addFile("icons/player.png", mode=QIcon.Mode.Selected)
            icon.addFile("icons/player.png", mode=QIcon.Mode.Disabled)
            self._q_icon = icon
        return self._q_icon

    @q_icon.setter
    def q_icon(self, icon: QIcon) -> None:
        self._q_icon = icon

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