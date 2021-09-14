from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QStandardItem

from model import World, Place, Object, ItemNode


class WorldController(QObject):

    item_deletion = pyqtSignal(QStandardItem)

    def __init__(self, model: World = None) -> None:
        super().__init__()
        self.model = model
        if self.model is None:
            self.__create_new_model()
    
    def __create_new_model(self, name: str = "New world") -> None:
        self.model = World()
        self.model.name = name

    @property
    def model(self) -> World:
        return self._model

    @model.setter
    def model(self, value: World) -> None:
        self._model = value

    def add_place(self) -> Place:
        count = self.model.places_count()
        place = Place(f"new_place{f'_{count}' if count != 0 else ''}")
        self.model.append_place(place)
        return place

    def add_object(self, container: ItemNode = None) -> Object:
        count = self.model.objects_count()
        object = Object(f"new_object{f'_{count}' if count != 0 else ''}")
        if container is not None:
            container.add_object(object)
        self.model.append_object(object)
        return object

    def remove_place(self, place: Place) -> None:
        self.model.remove_place(place.row())
        self.item_deletion.emit(place)