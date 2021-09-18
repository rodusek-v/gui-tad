from typing import List
from PyQt6.QtCore import QObject

from model import Command, Place, Object
from model.operation import FlagOperation, MessageOperation, OperationType


class CommandController(QObject):

    def __init__(self, model: Command) -> None:
        super().__init__()
        self._model = model

    @property
    def model(self) -> Command:
        return self._model

    @model.setter
    def model(self, value: Command) -> None:
        self._model = value

    def get_cmd_text(self) -> List[str]:
        return self.model.cmd_text

    def set_cmd_text(self, value: List[str]) -> None:
        self.model.cmd_text = value

    def get_type(self) -> OperationType:
        return self.model.operation.type

    def set_message(self, message: str) -> None:
        operation = self.model.operation
        if isinstance(operation, MessageOperation):
            operation.message = message
            
    def get_message(self) -> str:
        operation = self.model.operation
        if isinstance(operation, MessageOperation):
            return operation.message

    def set_item(self, item: 'Object') -> None:
        operation = self.model.operation
        if isinstance(operation, MessageOperation):
            operation.item = item

    def get_item(self) -> 'Object':
        operation = self.model.operation
        if isinstance(operation, MessageOperation):
            return operation.item

    def set_at(self, place: 'Place') -> None:
        operation = self.model.operation
        if isinstance(operation, MessageOperation) or isinstance(operation, FlagOperation):
            operation.at = place

    def get_at(self) -> 'Place':
        operation = self.model.operation
        if isinstance(operation, MessageOperation) or isinstance(operation, FlagOperation):
            return operation.at