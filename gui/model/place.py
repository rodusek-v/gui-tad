
from typing import List
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QIcon

from model.utils import Block, Description
from model.container import Container
from model.item_node import ItemNode


class Place(ItemNode, Container):

    def __init__(
        self,
        name:str = "new_place",
        description: Description = Description(),
        contains:List['Object'] = None,
        turns_in:int = None,
        blockade:List['Block'] = None,
    ) -> None:
        super().__init__()
        self.name = name
        self.description = description
        if contains is None:
            contains = []
        self.contains = contains
        self.turns_in = turns_in
        self.blockade = blockade

        self.position = None

        self.setEditable(False)

    @property
    def q_icon(self) -> QIcon:
        if self._q_icon is None:
            icon = QIcon()
            icon.addFile("icons/nodes/box.png", mode=QIcon.Mode.Active)
            icon.addFile("icons/nodes/box.png", mode=QIcon.Mode.Selected)
            icon.addFile("icons/nodes/box.png", mode=QIcon.Mode.Disabled)
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
        self.setText(self._name)

    @property
    def description(self) -> Description:
        return self._description

    @description.setter
    def description(self, value: Description) -> None:
        self._description = value

    @property
    def contains(self) -> List['Object']:
        return self._contains

    @contains.setter
    def contains(self, value: List['Object']) -> None:
        self._contains = value

    @property
    def turns_in(self) -> int:
        return self._turns_in

    @turns_in.setter
    def turns_in(self, value: int) -> None:
        self._turns_in = value

    @property
    def blockade(self) -> List[Block]:
        return self._blockade

    @blockade.setter
    def blockade(self, value: List[Block]) -> None:
        self._blockade = value

    @property
    def position(self) -> QRectF:
        return self._position

    @position.setter
    def position(self, position: QRectF):
        self._position = position

    def get_objects(self) -> List['Object']:
        return self.contains

    def add_object(self, object: 'Object') -> None:
        object.container = self
        self._contains.append(object)

    def remove_object(self, object: 'Object') -> None:
        try:
            self.contains.remove(object)
            del object.container
        except ValueError:
            pass

    

from model.object import Object