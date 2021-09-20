from PyQt6.QtCore import QObject

from model import Player


class PlayerController(QObject):

    def __init__(self, model: Player) -> None:
        super().__init__()
        self._model = model