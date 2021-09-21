import pickle

from typing import Dict, List
from PyQt6.QtCore import QObject, pyqtSignal

from model import *
from model.utils import Block, Dependency
from model.operation import CDMOperation, FlagOperation, MessageOperation, OperationType, RelocateOperation


class WorldController(QObject):

    item_deletion = pyqtSignal(ItemNode)
    item_addition = pyqtSignal(ItemNode)
    object_changes = pyqtSignal()
    not_allowed_delete = pyqtSignal(ItemNode)

    def __init__(self, model: World = None) -> None:
        super().__init__()
        self.model = model
        if self.model is None:
            self.__create_new_model()
        self.model.player.children_changed.connect(self.__container_change)
    
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

    def save(self):
        with open("test.dat", "wb") as dump:
            pickle.dump(self.model.serialize(), dump)

    def load(self):
        with open("test.dat", "rb") as dump:
            map: Dict[str, str] = pickle.load(dump)
            model = World()
            self.model = model
            model.load(map)

            places: Dict[str, Place] = {}
            for place in map['places']:
                place_model = self.add_place()
                place_model.load(place)
                places[place_model.name] = place_model

            objects: Dict[str, Object] = {}
            for object in map['objects']:
                object_model = self.add_object()
                object_model.load(object)
                objects[object_model.name] = object_model

            flags: Dict[str, Flag] = {}
            for flag in map['flags']:
                flag_model = self.add_flag()
                flag_model.load(flag)
                flags[flag_model.name] = flag_model

            commands: Dict[str, Command] = {}
            for command in map['commands']:
                command_model = self.add_command(command['_operation']['type'])
                command_model.load(command, places=places, objects=objects, flags=flags)
                commands[command_model.name] = command_model

            for conn in map['connections']:
                place_1 = places.get(conn['place_1'], None)
                place_2 = places.get(conn['place_2'], None)
                self.add_connection(place_1, conn['direction'], place_2)

            model.player.name = map['player']['_name']
            player_position = map['player']['_position']
            model.player.position = places.get(player_position, None)

            for obj in map['player']['_items']:
                model.player.add_object(objects[obj])

            finish_flag = map['finish']['_flag']
            model.finish.flag = flags.get(finish_flag, None)

            finish_position = map['finish']['_position']
            model.finish.position = places.get(finish_position, None)

            for place in map['places']:
                for obj in place['_contains']:
                    places[place['_name']].add_object(objects[obj])

                for block in place['_blockade']:
                    flag = flags[block['flag']]
                    flag.ref_count += 1
                    places[place['_name']].blockade.append(
                        Block(flag, block['direction'], block['turns']))

            for object in map['objects']:
                for obj in object['_contains']:
                    objects[object['_name']].add_object(objects[obj])

            for flg in map['flags']:
                for dep in flg['_action_on_true']['dependencies']:
                    flag = flags[dep['flag']]
                    flag.ref_count += 1
                    flags[flg['_name']].action_on_true.add_dependency(Dependency(flag, dep['value']))
                for dep in flg['_action_on_false']['dependencies']:
                    flag = flags[dep['flag']]
                    flag.ref_count += 1
                    flags[flg['_name']].action_on_false.add_dependency(Dependency(flag, dep['value']))

    def add_place(self) -> Place:
        index = self.model.places_index
        place = Place(f"new_place{f'_{index}' if index != 0 else ''}")
        self.model.append_place(place)
        place.children_changed.connect(self.__container_change)
        self.item_addition.emit(place)
        return place

    def add_object(self, container: Container = None) -> Object:
        index = self.model.objects_index
        object = Object(f"new_object{f'_{index}' if index != 0 else ''}")
        if container is not None:
            container.add_object(object)
        self.model.append_object(object)
        self.object_changes.emit()
        object.children_changed.connect(self.__container_change)
        self.item_addition.emit(object)
        return object

    def add_flag(self) -> Flag:
        index = self.model.flags_index
        flag = Flag(f"new_flag{f'_{index}' if index != 0 else ''}")
        self.model.append_flag(flag)
        self.item_addition.emit(flag)
        return flag

    def add_command(self, type: OperationType) -> Command:
        index = self.model.commands_index
        if type == OperationType.RELOCATION_OPERATION:
            operation = RelocateOperation()
        elif type == OperationType.FLAG_OPERATION:
            operation = FlagOperation()
        elif type == OperationType.CDM_OPERATION:
            operation = CDMOperation()
        else:
            operation = MessageOperation()
        cmd = Command(index, [f"new_command{f'_{index}' if index != 0 else ''}"], operation)
        self.model.append_command(cmd)
        self.item_addition.emit(cmd)
        return cmd

    def add_connection(self, conn: Connection):
        self.model.connections.append(conn)

    def remove_object(self, object: Object) -> bool:
        if object.ref_count == 0:
            self.model.remove_object(object.row())
            object.children_changed.disconnect(self.__container_change)
            self.object_changes.emit()
            self.item_deletion.emit(object)
            return True
        
        self.not_allowed_delete.emit(object)
        return False

    def remove_place(self, place: Place) -> bool:
        if place.ref_count == 0:
            self.model.remove_place(place.row())
            place.children_changed.disconnect(self.__container_change)
            self.object_changes.emit()
            self.item_deletion.emit(place)
            return True
        
        self.not_allowed_delete.emit(place)
        return False

    def remove_flag(self, flag: Flag) -> bool:
        if flag.ref_count == 0:
            self.model.remove_flag(flag.row())
            self.item_deletion.emit(flag)
            return True
        
        self.not_allowed_delete.emit(flag)
        return False

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
        containers.append(self.model.player)
        return containers

    def get_player(self) -> 'Player':
        return self.model.player

    def get_finish(self) -> 'Finish':
        return self.model.finish
