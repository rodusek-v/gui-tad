from typing import List
from PyQt6.QtGui import QIcon, QStandardItem

from model.place import Place
from model.object import Object
from model.flag import Flag
from model.command import Command
from model.player import Player
from model.finish import Finish
from model.connection import Connection
from model.helpers import TextModel
from constants import THIS_FOLDER


class World(QStandardItem, TextModel):

    def __init__(self) -> None:
        super().__init__()
        self._name = None
        self._connections: List['Connection'] = []
        self._player = Player("PLAYER")
        self._finish = Finish()

        self._places_index = 0
        self._objects_index = 0
        self._flags_index = 0
        self._commands_index = 0

        self.template_path = "template/world.template"
        self.setIcon(QIcon("/".join([THIS_FOLDER, "icons/map.png"])))
        self.setEditable(False)
        self.__init_model()

    def __init_model(self):
        self._places = World.__create_folder_item(self.__create_icon("icons/box.png"), 'Places')
        self._objects = World.__create_folder_item(self.__create_icon("icons/object.png"), 'Objects')
        self._commands = World.__create_folder_item(self.__create_icon("icons/command.png"), 'Commands')
        self._flags = World.__create_folder_item(self.__create_icon("icons/flag.png"), 'Flags')
        self.appendRows([
            self._places, 
            self._objects, 
            self._commands, 
            self._flags
        ])

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.setText(self._name)

    @property
    def places(self) -> List['Place']:
        temp = self._places
        return [temp.child(i) for i in range(temp.rowCount())]

    @property
    def objects(self):
        temp = self._objects
        return [temp.child(i) for i in range(temp.rowCount())]

    @property
    def commands(self):
        temp = self._commands
        return [temp.child(i) for i in range(temp.rowCount())]

    @property
    def flags(self):
        temp = self._flags
        return [temp.child(i) for i in range(temp.rowCount())]

    @property
    def connections(self) -> List['Connection']:
        return self._connections

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, player):
        self._player = player

    @property
    def finish(self):
        return self._finish
    
    @finish.setter
    def finish(self, finish):
        self._finish = finish

    def load(self, desereliazed):
        self._places_index = desereliazed['places_index']
        self._objects_index = desereliazed['objects_index']
        self._flags_index = desereliazed['flags_index']
        self._commands_index = desereliazed['commands_index']

    def append_place(self, place):
        self._places.appendRow(place)
        self._places_index += 1

    def remove_place(self, row_num):
        row = self._places.takeRow(row_num)
        if len(row) != 0 and isinstance(row[0], Place):
            for obj in row[0].get_objects():
                del obj.container
            for block in row[0].blockade:
                block.flag.ref_count -= 1

    def append_object(self, object):
        self._objects.appendRow(object)
        self._objects_index += 1

    def remove_object(self, row_num):
        row = self._objects.takeRow(row_num)
        if len(row) != 0 and isinstance(row[0], Object):
            if row[0].container is not None:
                row[0].container.remove_object(row[0])

    def append_flag(self, flag):
        self._flags.appendRow(flag)
        self._flags_index += 1

    def remove_flag(self, row_num):
        row = self._flags.takeRow(row_num)
        if len(row) != 0 and isinstance(row[0], Flag):
            for d in row[0].action_on_true.get_dependencies():
                d.flag.ref_count -= 1
            for d in row[0].action_on_false.get_dependencies():
                d.flag.ref_count -= 1

    def append_command(self, command):
        self._commands.appendRow(command)
        self._commands_index += 1

    def remove_command(self, row_num):
        row = self._commands.takeRow(row_num)
        if len(row) != 0 and isinstance(row[0], Command):
            row[0].operation.decrease_refferees()

    @property
    def places_index(self) -> int:
        return self._places_index

    @property
    def objects_index(self) -> int:
        return self._objects_index

    @property
    def flags_index(self) -> int:
        return self._flags_index

    @property
    def commands_index(self) -> int:
        return self._commands_index

    @staticmethod
    def __create_folder_item(icon: QIcon, text: str):
        item = QStandardItem(icon, text)
        item.setEditable(False)

        return item

    @staticmethod
    def __create_icon(path: str) -> QIcon:
        icon = QIcon()
        path = "/".join([THIS_FOLDER, path])
        icon.addFile(path, mode=QIcon.Mode.Active)
        icon.addFile(path, mode=QIcon.Mode.Selected)
        icon.addFile(path, mode=QIcon.Mode.Disabled)

        return icon
