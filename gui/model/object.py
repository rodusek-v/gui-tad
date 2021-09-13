from typing import List
from PyQt6.QtGui import QIcon, QStandardItem

from model.utils import Description
from model.item_node import ItemNode


class Object(QStandardItem, ItemNode):

    def __init__(
        self,
        name:str = "new_object",
        description: Description = Description(),
        contains:List['Object'] = list(),
        pickable:bool = None,
        container:ItemNode = None
    ) -> None:
        super().__init__()
        self.name = name
        self.description = description
        self.contains = contains
        self.pickable = pickable
        self.container = container
        
        icon = QIcon()
        icon.addFile("icons/nodes/object.png", mode=QIcon.Mode.Active)
        icon.addFile("icons/nodes/object.png", mode=QIcon.Mode.Disabled)
        self.setIcon(icon)
        self.setEditable(False)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value
        self.setText(self._name)

    @property
    def description(self) -> Description:
        return self._description

    @description.setter
    def description(self, value: Description):
        self._description = value

    @property
    def contains(self) -> List['Object']:
        return self._contains

    @contains.setter
    def contains(self, value: List['Object']):
        self._contains = value

    @property
    def pickable(self) -> bool:
        return self._pickable

    @pickable.setter
    def pickable(self, value: bool):
        self._pickable = value

    @property
    def container(self) -> ItemNode:
        return self._container

    @container.setter
    def container(self, value: ItemNode):
        self._container = value

    def add_object(self, object: 'Object') -> None:
        object.container = self
        self._contains.append(object)

    def get_objects(self) -> List['Object']:
        return self.contains

    def free(self):
        self._container = None
