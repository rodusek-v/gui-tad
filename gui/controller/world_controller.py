import json

from typing import Dict, List
from textx import metamodel_from_file
from PyQt6.QtCore import QObject, QRectF, pyqtSignal

from model import *
from model.utils import Block, Dependency
from model.operation import CDMOperation, FlagOperation, MessageOperation, OperationType, RelocateOperation
from config_loader import Config


class WorldController(QObject):

    item_deletion = pyqtSignal(ItemNode)
    item_addition = pyqtSignal(ItemNode)
    object_changes = pyqtSignal()
    not_allowed_delete = pyqtSignal(ItemNode)

    def __init__(self, model: World = None) -> None:
        super().__init__()
        self.config = Config()
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

    def load(self):
        path = self.config.get_last_loaded()
        world_config = path.replace(".wld", ".json")
        meta_model = metamodel_from_file("../textx/tad_meta.tx")
        try:
            model = meta_model.model_from_file(path)
            world = World()
            world.name = model.name
            self.model = world

            places: Dict[str, Place] = {}
            for place in model.places:
                place_model = self.add_place()
                place_model.load(place)
                places[place_model.name] = place_model
                
            objects: Dict[str, Object] = {}
            for object in model.objects:
                object_model = self.add_object()
                object_model.load(object)
                objects[object_model.name] = object_model

            flags: Dict[str, Flag] = {}
            for flag in model.flags:
                flag_model = self.add_flag()
                flag_model.load(flag)
                flags[flag_model.name] = flag_model

            commands: Dict[str, Command] = {}
            for command in model.commands:
                operation_type = OperationType(command.operation.__class__.__name__)
                command_model = self.add_command(operation_type)
                command_model.load(command, places=places, objects=objects, flags=flags)
                commands[command_model.name] = command_model

            for conn in model.connections:
                place_1 = places.get(conn.from_.name, None)
                place_2 = places.get(conn.to_.name, None)
                self.add_connection(place_1, Sides(conn.direction), place_2)
        
            world.player.name = model.player.name
            player_position = None
            if model.player.position:
                player_position = model.player.position.name
            world.player.position = places.get(player_position, None)

            for obj in model.player.items:
                world.player.add_object(objects[obj.name])

            finish_flag = None
            value = False
            if model.finish.flag_prop:
                finish_flag = model.finish.flag_prop.flag.name
                value = model.finish.flag_prop.value
            world.finish.flag = flags.get(finish_flag, None)
            finish_position = None
            if model.finish.position:
                finish_position = model.finish.position.name
            world.finish.position = places.get(finish_position, None)
            world.finish.value = value

            for place in model.places:
                for obj in place.contains.objects:
                    places[place.name].add_object(objects[obj.name])

                if place.blockade:
                    for block in place.blockade.blocks:
                        flag = flags[block.flag.name]
                        flag.ref_count += 1
                        turn = -1
                        if block.turns:
                            turn = block.turns.value
                        places[place.name].blockade.append(
                            Block(flag, Sides(block.direction), turn))

            for object in model.objects:
                for obj in object.contains.objects:
                    objects[object.name].add_object(objects[obj.name])

            for flg in model.flags:
                true_dependencies = []
                if flg.action_true.dependencies:
                    true_dependencies = flg.action_true.dependencies
                for dep in true_dependencies:
                    flag = flags[dep.flag.name]
                    flag.ref_count += 1
                    flags[flg.name].action_on_true.add_dependency(Dependency(flag, dep.value))

                false_dependencies = []
                if flg.action_false.dependencies:
                    true_dependencies = flg.action_false.dependencies
                for dep in false_dependencies:
                    flag = flags[dep.flag.name]
                    flag.ref_count += 1
                    flags[flg.name].action_on_false.add_dependency(Dependency(flag, dep.value))
        except Exception as ex:
            print(ex)

        try:
            with open(world_config, "r") as conf_file:
                configs = json.load(conf_file)
                world.load(configs)
                for key, value in configs['positions'].items():
                    places[key].position = QRectF(value[0], value[1], value[2], value[3])
        except Exception as ex:
            with open(world_config, "w") as conf_file:
                conf = self.get_current_conf()
                json.dump(conf, conf_file, indent=4)

    def save(self):
        meta_model = metamodel_from_file("../textx/world.tx")
        path = self.config.get_last_loaded()
        world_config = path.replace(".wld", ".json")
        try:
            with open(world_config, "w") as conf_file:
                conf = self.get_current_conf()
                json.dump(conf, conf_file, indent=4)
            with open(path, "w") as file:
                lines = self.model.text_model().split("\n")
                new_text = "\n".join([line for line in lines if line.strip() != ""])
                file.write(new_text)
                meta_model.model_from_str(new_text)
        except Exception as ex:
            raise Exception(ex)

    def get_current_conf(self):
        return {
            "places_index": self.model.places_index,
            "objects_index": self.model.objects_index,
            "flags_index": self.model.flags_index,
            "commands_index": self.model.commands_index,
            "positions": {
                place.name : place.position.getRect() for place in self.model.places
            },
        }
        
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
        cmd = Command([f"new_command{f'_{index}' if index != 0 else ''}"], operation)
        self.model.append_command(cmd)
        self.item_addition.emit(cmd)
        return cmd

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
            if self.model.player.position == place:
                self.model.player.position = None
            if self.model.finish.position == place:
                self.model.finish.position = None
            place.children_changed.disconnect(self.__container_change)
            self.object_changes.emit()
            self.item_deletion.emit(place)
            return True
        
        self.not_allowed_delete.emit(place)
        return False

    def remove_flag(self, flag: Flag) -> bool:
        if flag.ref_count == 0:
            self.model.remove_flag(flag.row())
            if self.model.finish.flag == flag:
                self.model.finish.flag = None
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
