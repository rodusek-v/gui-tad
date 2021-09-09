from PyQt6.QtGui import QIcon, QStandardItem

class Place(QStandardItem):

    def __init__(
        self,
        name=None,
        description=None,
        contains=None,
        turns_in=None,
        blockade=None,
        parent=None
    ) -> None:
        super().__init__()
        self.name = name
        self.description = description
        self.contains = contains
        self.turns_in = turns_in
        self.blockade = blockade
        