from PyQt6.QtCore import QObject

class Finish(QObject):

    def __init__(
        self,
        position=None,
        flag=None
    ) -> None:
        super().__init__()
        self.position = position
        self.flag = flag