from typing import List
from PyQt6.QtCore import QObject

from model import Object, Container


class ObjectController(QObject):

    def __init__(self, model: Object) -> None:
        super().__init__()
        self._model = model

    @property
    def model(self) -> Object:
        return self._model

    @model.setter
    def model(self, value: Object) -> None:
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

    def set_pickable(self, pickable: bool) -> None:
        self.model.pickable = pickable

    def get_pickable(self) -> bool:
        return self.model.pickable

    def set_container(self, new: Container) -> None:
        old = self.model.container
        if old is not None:
            old.remove_object(self.model)
            old.children_changed.emit()
        if new is not None:
            if isinstance(new, Object) and new in self.model.contains:
                self.model.contains.remove(new)
                new.container = None
            new.add_object(self.model)
            new.children_changed.emit()
        else:
            self.model.container = None
            
    def get_container(self) -> Container:
        return self.model.container

    def get_contains(self) -> List['Object']:
        return self.model.contains
            