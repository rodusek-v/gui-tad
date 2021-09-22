from typing import List
from PyQt6.QtCore import QObject

from model import Player, Place, Object


class PlayerController(QObject):

    def __init__(self, model: Player) -> None:
        super().__init__()
        self._model = model

    @property
    def model(self) -> Player:
        return self._model

    @model.setter
    def model(self, value: Player) -> None:
        self._model = value

    def set_name(self, value: str) -> None:
        self.model.name = value.upper()

    def get_name(self) -> str:
        return self.model.name

    def set_position(self, value: 'Place') -> None:
        self.model.position = value 

    def get_position(self) -> 'Place':
        return self.model.position
    
    def get_items(self) -> List['Object']:
        return self.model.get_objects()

    def assign_objects(self, objects: List['Object']) -> None:
        for obj in objects:
            old = obj.container
            if old is not None:
                old.remove_object(obj)
                old.children_changed.emit()
            self.model.add_object(obj)
        self.model.children_changed.emit()

    def free_objects(self, objects: List['Object']) -> None:
        for obj in objects:
            old = obj.container
            if old is not None:
                old.remove_object(obj)
                old.children_changed.emit()
        self.model.children_changed.emit()