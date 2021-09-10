from PyQt6.QtGui import QStandardItem

class Flag(QStandardItem):

    def __init__(
        self,
        name=None,
        activated=None,
        action_on_true=None,
        action_on_false=None
    ) -> None:
        super().__init__()
        self.name = name
        self.activated = activated
        self.action_on_true = action_on_true
        self.action_on_false = action_on_false