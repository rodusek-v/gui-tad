
from typing import List
from PyQt6.QtGui import QIcon, QStandardItem

from model.utils import Block, Description


class Place(QStandardItem):

    def __init__(
        self,
        name:str = "new_place",
        description: Description = Description(),
        contains:List['Object'] = list(),
        turns_in:int = None,
        blockade:List['Block'] = None,
    ) -> None:
        super().__init__()
        self.name = name
        self.description = description
        self.contains = contains
        self.turns_in = turns_in
        self.blockade = blockade

        self.setIcon(QIcon("icons/nodes/box.png"))
        
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
    def turns_in(self) -> int:
        return self._turns_in

    @turns_in.setter
    def turns_in(self, value: int):
        self._turns_in = value

    @property
    def blockade(self) -> List[Block]:
        return self._blockade

    @blockade.setter
    def blockade(self, value: List[Block]):
        self._blockade = value
    

from model.object import Object