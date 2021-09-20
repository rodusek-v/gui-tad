from PyQt6.QtGui import QIcon, QStandardItem

from model.place import Place
from model.object import Object
from model.flag import Flag
from model.command import Command
from model.player import Player
from model.finish import Finish
from model.utils import TextModel


class World(QStandardItem, TextModel):

    def __init__(self) -> None:
        super().__init__()
        self._name = None
        self._description = None
        self._connections = list()
        self._player = Player("player")
        self._finish = Finish()

        self._places_count = 0
        self._objects_count = 0
        self._flags_count = 0
        self._commands_count = 0

        self.setIcon(QIcon("icons/map.png"))
        self.setEditable(False)
        self.__append_all_childrens()

    def __append_all_childrens(
        self,
        places=list(),
        objects=list(),
        flags=list(),
        commands=list()
    ):
        self._places = World.__create_folder_item(self.__create_icon("icons/box.png"), 'Places')
        self._places.appendRows(places)
        self._objects = World.__create_folder_item(self.__create_icon("icons/object.png"), 'Objects')
        self._objects.appendRows(objects)
        self._commands = World.__create_folder_item(self.__create_icon("icons/command.png"), 'Commands')
        self._commands.appendRows(commands)
        self._flags = World.__create_folder_item(self.__create_icon("icons/flag.png"), 'Flags')
        self._flags.appendRows(flags)
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
    def places(self):
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
    def connections(self):
        return self._connections

    @property
    def player(self):
        return self._player

    @property
    def finish(self):
        return self._finish

    def save(self):
        pass

    def append_place(self, place):
        self._places.appendRow(place)
        self._places_count += 1

    def remove_place(self, row_num):
        row = self._places.takeRow(row_num)
        if len(row) != 0 and isinstance(row[0], Place):
            for obj in row[0].get_objects():
                del obj.container
            for block in row[0].blockade:
                block.flag.ref_count -= 1

    def append_object(self, object):
        self._objects.appendRow(object)
        self._objects_count += 1

    def remove_object(self, row_num):
        row = self._objects.takeRow(row_num)
        if len(row) != 0 and isinstance(row[0], Object):
            if row[0].container is not None:
                row[0].container.remove_object(row[0])

    def append_flag(self, flag):
        self._flags.appendRow(flag)
        self._flags_count += 1

    def remove_flag(self, row_num):
        row = self._flags.takeRow(row_num)
        if len(row) != 0 and isinstance(row[0], Flag):
            for d in row[0].action_on_true.get_dependecines():
                d.flag.ref_count -= 1
            for d in row[0].action_on_false.get_dependecines():
                d.flag.ref_count -= 1

    def append_command(self, command):
        self._commands.appendRow(command)
        self._commands_count += 1

    def remove_command(self, row_num):
        row = self._commands.takeRow(row_num)
        if len(row) != 0 and isinstance(row[0], Command):
            row[0].operation.decrease_refferees()

    def places_count(self) -> int:
        return self._places_count

    def objects_count(self) -> int:
        return self._objects_count

    def flags_count(self) -> int:
        return self._flags_count

    def commands_count(self) -> int:
        return self._commands_count

    @staticmethod
    def __create_folder_item(icon: QIcon, text: str):
        item = QStandardItem(icon, text)
        item.setEditable(False)

        return item

    @staticmethod
    def __create_icon(path: str) -> QIcon:
        icon = QIcon()
        icon.addFile(path, mode=QIcon.Mode.Active)
        icon.addFile(path, mode=QIcon.Mode.Selected)
        icon.addFile(path, mode=QIcon.Mode.Disabled)

        return icon
