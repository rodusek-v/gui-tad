from PyQt6.QtGui import QStandardItem

class Object(QStandardItem):

    def __init__(
        self,
        name=None,
        description=None,
        contains=None,
        pickable=None,
        container=None,
        parent=None
    ) -> None:
        super().__init__()
        self.name = name
        self.description = description
        self.contains = contains
        self.pickable = pickable
        self.container = container