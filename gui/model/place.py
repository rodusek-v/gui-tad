
from typing import List
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QIcon

from model.container import Container
from model.item_node import ItemNode
from constants import THIS_FOLDER


class Place(ItemNode, Container):

    def __init__(
        self,
        name:str = "new_place",
        description: 'Description' = None,
        contains: List['Object'] = None,
        blockade: List['Block'] = None
    ) -> None:
        super().__init__()
        self.name = name
        if description is None:
            description = Description()
        self.description = description
        if contains is None:
            contains = []
        self.contains = contains
        if blockade is None:
            blockade = []
        self.blockade = blockade

        self.position = None

    @property
    def q_icon(self) -> QIcon:
        if self._q_icon is None:
            icon = QIcon()
            png_path = "/".join([THIS_FOLDER, "icons/nodes/box.png"])
            icon.addFile(png_path, mode=QIcon.Mode.Active)
            icon.addFile(png_path, mode=QIcon.Mode.Selected)
            icon.addFile(png_path, mode=QIcon.Mode.Disabled)
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
        self.rename_signal.emit()

    @property
    def description(self) -> 'Description':
        return self._description

    @description.setter
    def description(self, value: 'Description') -> None:
        self._description = value

    @property
    def contains(self) -> List['Object']:
        return self._contains

    @contains.setter
    def contains(self, value: List['Object']) -> None:
        self._contains = value

    @property
    def blockade(self) -> List['Block']:
        return self._blockade

    @blockade.setter
    def blockade(self, value: List['Block']) -> None:
        self._blockade = value

    @property
    def position(self) -> QPointF:
        return self._position

    @position.setter
    def position(self, position: QPointF):
        self._position = position

    def load(self, model):
        self.name = model.name
        self.description.name = model.description.name
        self.description.description = model.description.description

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
from model.utils import Block, Description