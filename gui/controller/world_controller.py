from typing import List
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QStandardItem

from model import World, Place, Object, Container


class WorldController(QObject):

    item_deletion = pyqtSignal(QStandardItem)
    object_changes = pyqtSignal()

    def __init__(self, model: World = None) -> None:
        super().__init__()
        self.model = model
        if self.model is None:
            self.__create_new_model()
    
    def __create_new_model(self, name: str = "New world") -> None:
        self.model = World()
        self.model.name = name

    def __container_change(self):
        self.object_changes.emit()

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
        place.children_changed.connect(self.__container_change)
        return place

    def add_object(self, container: Container = None) -> Object:
        count = self.model.objects_count()
        object = Object(f"new_object{f'_{count}' if count != 0 else ''}")
        if container is not None:
            container.add_object(object)
        self.model.append_object(object)
        self.object_changes.emit()
        return object

    def remove_object(self, object: Object) -> None:
        self.model.remove_object(object.row())
        self.object_changes.emit()
        self.item_deletion.emit(object)

    def remove_place(self, place: Place) -> None:
        self.model.remove_place(place.row())
        place.children_changed.disconnect(self.__container_change)
        self.item_deletion.emit(place)

    def get_objects(self) -> List['Object']:
        return self.model.objects

    def get_places(self) -> List['Place']:
        return self.model.places

    def get_containers(self) -> List['Container']:
        containers = []
        containers.extend(self.model.places)
        containers.extend(self.model.objects)
        # containers.append(self.model.player) TODO: initialize player
        return containers