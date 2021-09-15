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

    def set_turns_in(self, turns_in: str) -> None:
        num = None
        try:
            num = int(turns_in)
        except:
            pass
        self.model.turns_in = num

    def get_turns_in(self) -> str:
        return "" if self.model.turns_in is None else str(self.model.turns_in)
            