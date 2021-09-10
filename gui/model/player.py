from PyQt6.QtCore import QObject

class Player(QObject):

    def __init__(
        self,
        name=None,
        position=None,
        items=list()
    ) -> None:
        super().__init__()
        self.name = name
        self.position = position
        self.items = items