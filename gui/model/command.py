from PyQt6.QtGui import QStandardItem


class Command(QStandardItem):

    def __init__(
        self, 
        text=None,
        operation=None
    ) -> None:
        super().__init__()
        self.cmd_text = text
        self.operation = operation
