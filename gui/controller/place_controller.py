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

    def set_name(self, name: str) -> None:
        self.model.name = name

    def get_name(self) -> str:
        return self.model.name

    def set_descriptive_name(self, name: str) -> None:
        self.model.description.name = name

    def get_descriptive_name(self) -> str:
        return self.model.description.name

    def set_description(self, description: str) -> None:
        self.model.description.description = description

    def get_description(self) -> str:
        return self.model.description.description

    def get_contains(self) -> List['Object']:
        return self.model.contains
            