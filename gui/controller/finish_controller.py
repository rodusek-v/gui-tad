from PyQt6.QtCore import QObject

from model import Finish, Place, Flag


class FinishController(QObject):

    def __init__(self, model: Finish) -> None:
        super().__init__()
        self._model = model

    @property
    def model(self) -> Finish:
        return self._model

    @model.setter
    def model(self, value: Finish) -> None:
        self._model = value

    def set_position(self, value: 'Place') -> None:
        self.model.position = value 

    def get_position(self) -> 'Place':
        return self.model.position

    def set_flag(self, value: 'Flag') -> None:
        self.model.flag = value 

    def get_flag(self) -> 'Flag':
        return self.model.flag

    def set_value(self, value: bool) -> None:
        self.model.value = value 

    def get_value(self) -> bool:
        return self.model.value