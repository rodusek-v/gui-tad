from typing import List
from PyQt6.QtCore import QObject, pyqtSignal

from model import World, Place, Object, Container, Flag, Command, ItemNode, Connection, Sides, Connection
from model.operation import CDMOperation, FlagOperation, MessageOperation, OperationType, RelocateOperation


class WorldController(QObject):

    item_deletion = pyqtSignal(ItemNode)
    item_addition = pyqtSignal(ItemNode)
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
        self.item_addition.emit(place)
        return place

    def add_object(self, container: Container = None) -> Object:
        count = self.model.objects_count()
        object = Object(f"new_object{f'_{count}' if count != 0 else ''}")
        if container is not None:
            container.add_object(object)
        self.model.append_object(object)
        self.object_changes.emit()
        object.children_changed.connect(self.__container_change)
        self.item_addition.emit(object)
        return object

    def add_flag(self) -> Flag:
        count = self.model.flags_count()
        flag = Flag(f"new_flag{f'_{count}' if count != 0 else ''}")
        self.model.append_flag(flag)
        self.item_addition.emit(flag)
        return flag

    def add_command(self, type: OperationType) -> Command:
        count = self.model.commands_count()
        if type == OperationType.RELOCATION_OPERATION:
            operation = RelocateOperation()
        elif type == OperationType.FLAG_OPERATION:
            operation = FlagOperation()
        elif type == OperationType.CDM_OPERATION:
            operation = CDMOperation()
        else:
            operation = MessageOperation()
        cmd = Command(count, [f"new_command{f'_{count}' if count != 0 else ''}"], operation)
        self.model.append_command(cmd)
        self.item_addition.emit(cmd)
        return cmd

    def add_connection(self, conn: Connection):
        self.model.connections.append(conn)

    def remove_object(self, object: Object) -> None:
        self.model.remove_object(object.row())
        object.children_changed.disconnect(self.__container_change)
        self.object_changes.emit()
        self.item_deletion.emit(object)

    def remove_place(self, place: Place) -> None:
        self.model.remove_place(place.row())
        place.children_changed.disconnect(self.__container_change)
        self.object_changes.emit()
        self.item_deletion.emit(place)

    def remove_flag(self, flag: Flag) -> None:
        self.model.remove_flag(flag.row())
        self.item_deletion.emit(flag)

    def remove_cmd(self, cmd: Command) -> None:
        self.model.remove_command(cmd.row())
        self.item_deletion.emit(cmd)

    def remove_connection(self, conn: Connection):
        self.model.connections.remove(conn)

    def get_objects(self) -> List['Object']:
        return self.model.objects

    def get_places(self) -> List['Place']:
        return self.model.places

    def get_flags(self) -> List['Flag']:
        return self.model.flags

    def get_connections(self) -> List['Connection']:
        return self.model.connections

    def add_connection(self, place_1: 'Place', direction: Sides, place_2: 'Place') -> None:
        self.model.connections.append(Connection(place_1, direction, place_2))

    def remove_connection(self, place_1: 'Place', direction: Sides, place_2: 'Place') -> None:
        self.model.connections.remove(Connection(place_1, direction, place_2))

    def get_containers(self) -> List['Container']:
        containers = []
        containers.extend(self.model.places)
        containers.extend(self.model.objects)
        # containers.append(self.model.player) TODO: initialize player
        return containers