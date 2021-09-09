from PyQt6.QtGui import QStandardItem

class Command(QStandardItem):

    def __init__(
        self, 
        text=None,
        operation=None,
        parent=None
    ) -> None:
        super().__init__()
        self.cmd_text = text
        self.operation = operation

class Operation(object):

    def __init__(self, parent) -> None:
        super().__init__()