from typing import List
from PyQt6.QtGui import QIcon

from model.operation import Operation
from model.item_node import ItemNode


class Command(ItemNode):

    def __init__(
        self,
        id: int,
        text: List[str] = None,
        operation: Operation = None
    ) -> None:
        super().__init__()
        self._id = id
        if text is None:
            text = []
        self.cmd_text = text
        self.operation = operation

    @property
    def q_icon(self) -> QIcon:
        if self._q_icon is None:
            icon = QIcon()
            icon.addFile("icons/nodes/command.png", mode=QIcon.Mode.Active)
            icon.addFile("icons/nodes/command.png", mode=QIcon.Mode.Selected)
            icon.addFile("icons/nodes/command.png", mode=QIcon.Mode.Disabled)
            self._q_icon = icon
        return self._q_icon

    @q_icon.setter
    def q_icon(self, icon: QIcon) -> None:
        self._q_icon = icon

    @property
    def id(self) -> int:
        return self._id

    @property
    def cmd_text(self) -> List[str]:
        return self._cmd_text

    @cmd_text.setter
    def cmd_text(self, value: List[str]) -> None:
        self._cmd_text = value
        self.setText(", ".join(self._cmd_text[:3]))

    @property
    def operation(self) -> Operation:
        return self._operation

    @operation.setter
    def operation(self, value: Operation) -> None:
        self._operation = value
