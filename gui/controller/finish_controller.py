from PyQt6.QtCore import QObject

from model import Finish


class FinishController(QObject):

    def __init__(self, model: Finish) -> None:
        super().__init__()
        self._model = model