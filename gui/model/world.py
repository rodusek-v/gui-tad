from model.item_node import ItemNode
from model.utils import TextModel
from PyQt6.QtGui import QIcon, QStandardItem

class World(QStandardItem, TextModel):

    def __init__(self) -> None:
        super().__init__()
        self._name = None
        self._description = None
        self._connections = list()
        self._player = None
        self._finish = None

        self._places_count = 0
        self._objects_count = 0

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
        self._places = World.__create_folder_item(QIcon("icons/box.png"), 'Places')
        self._places.appendRows(places)
        self._objects = World.__create_folder_item(QIcon("icons/object.png"), 'Objects')
        self._objects.appendRows(objects)
        self._commands = World.__create_folder_item(QIcon("icons/command.png"), 'Commands')
        self._commands.appendRows(commands)
        self._flags = World.__create_folder_item(QIcon("icons/flag.png"), 'Flags')
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

    def save(self):
        pass

    def append_place(self, place):
        self._places.appendRow(place)
        self._places_count += 1

    def remove_place(self, row_num):
        row = self._places.takeRow(row_num)
        if len(row) != 0 and isinstance(row[0], ItemNode):
            for obj in row[0].get_objects():
                del obj.container

    def append_object(self, object):
        self._objects.appendRow(object)
        self._objects_count += 1

    def append_command(self, command):
        self._commands.appendRow(command)

    def append_flag(self, flag):
        self._flags.appendRow(flag)

    def places_count(self) -> int:
        return self._places_count

    def objects_count(self) -> int:
        return self._objects_count

    @staticmethod
    def __create_folder_item(icon: QIcon, text: str):
        item = QStandardItem(icon, text)
        item.setEditable(False)

        return item
