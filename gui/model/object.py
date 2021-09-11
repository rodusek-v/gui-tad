from typing import Union, List
from PyQt6.QtGui import QIcon, QStandardItem

from model.utils import Description


class Object(QStandardItem):

    def __init__(
        self,
        name:str = "new_object",
        description: Description = Description(),
        contains:List['Object'] = list(),
        pickable:bool = None,
        container:Union['Place', 'Object', 'Player'] = None
    ) -> None:
        super().__init__()
        self.name = name
        self.description = description
        self.contains = contains
        self.pickable = pickable
        self.container = container

        self.setIcon(QIcon("icons/nodes/object.png"))
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
    def container(self) -> Union['Place', 'Object', 'Player']:
        return self._container

    @container.setter
    def container(self, value: Union['Place', 'Object', 'Player']):
        self._container = value


from model.place import Place
from model.player import Player