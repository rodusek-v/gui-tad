from typing import List
from PyQt6.QtCore import QObject

from model import Place, Object


class PlaceController(QObject):

    def __init__(self, model: Place) -> None:
        super().__init__()
        self._model = model

    @property
    def model(self) -> Place:
        return self._model

    @model.setter
    def model(self, value: Place) -> None:
        self._model = value

    def assign_objects(self, old: Place, objects: List['Object']) -> None:
        for obj in objects:
            old.remove_object(obj)
            self.model.add_object(obj)
            