
from typing import List
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QIcon

from model.container import Container
from model.item_node import ItemNode


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
    def position(self) -> QRectF:
        return self._position

    @position.setter
    def position(self, position: QRectF):
        self._position = position

    def serialize(self):
        ser = dict(self.__dict__)
        del ser['_q_icon']
        del ser['_ItemNode__signaler']
        del ser['_ref_count']
        ser['_description'] = self.description.__dict__
        ser['_contains'] = [obj.name for obj in self.contains]
        ser['_blockade'] = [block.serialize() for block in self.blockade]
        return ser

    def load(self, serialized):
        self.name = serialized['_name']
        self.description.name = serialized['_description']['name']
        self.description.description = serialized['_description']['description']
        self.position = QRectF(serialized['_position'])

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