from typing import List
from PyQt6.QtGui import QIcon

from model.utils import Description
from model.container import Container
from model.item_node import ItemNode


class Object(ItemNode, Container):

    def __init__(
        self,
        name:str = "new_object",
        description: Description = Description(),
        contains:List['Object'] = list(),
        pickable:bool = None,
        container:Container = None
    ) -> None:
        super().__init__()
        self.name = name
        self.description = description
        self.contains = contains
        self.pickable = pickable
        self.container = container
        self.setEditable(False)

    @property
    def q_icon(self) -> QIcon:
        if self._q_icon is None:
            icon = QIcon()
            icon.addFile("icons/nodes/object.png", mode=QIcon.Mode.Active)
            icon.addFile("icons/nodes/object.png", mode=QIcon.Mode.Selected)
            icon.addFile("icons/nodes/object.png", mode=QIcon.Mode.Disabled)
            self._q_icon = icon
        return self._q_icon

    @q_icon.setter
    def q_icon(self, icon: QIcon) -> None:
        self._q_icon = icon

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
    def container(self) -> Container:
        return self._container

    @container.setter
    def container(self, value: Container):
        self._container = value

    @container.deleter
    def container(self):
        self._container = None

    def add_object(self, object: 'Object') -> None:
        object.container = self
        self._contains.append(object)

    def get_objects(self) -> List['Object']:
        return self.contains

    def remove_object(self, object: 'Object') -> None:
        try:
            self.contains.remove(object)
            del object.container
        except ValueError:
            pass
