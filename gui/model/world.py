from PyQt6.QtGui import QIcon, QStandardItem

class World(QStandardItem):

    def __init__(
        self,
        name=None,
        description=None,
        places=list(),
        objects=list(),
        connections=list(),
        commands=list(),
        flags=list(),
        player=None,
        finish=None,
        parent=None
    ) -> None:
        super().__init__()
        self.name = name
        self.description = description
        self.places = places
        self.objects = objects
        self.connections = connections
        self.commands = commands
        self.flag_list = flags
        self.player = player
        self.finish = finish

        self.setText(self.name)
        self.setIcon(QIcon("icons/map.png"))
        self.setEditable(False)
        self.__append_all_childrens()
        
    def __append_all_childrens(self):
        places = World.__create_folder_item(QIcon("icons/box.png"), 'Places')
        places.appendRows(self.places)
        objects = World.__create_folder_item(QIcon("icons/object.png"), 'Objects')
        objects.appendRows(self.objects)
        commands = World.__create_folder_item(QIcon("icons/command.png"), 'Commands')
        commands.appendRows(self.commands)
        flags = World.__create_folder_item(QIcon("icons/flag.png"), 'Flags')
        flags.appendRows(self.flag_list)

        self.appendRows([places, objects, commands, flags])

    @staticmethod
    def __create_folder_item(icon: QIcon, text: str):
        item = QStandardItem(icon, text)
        item.setEditable(False)

        return item
