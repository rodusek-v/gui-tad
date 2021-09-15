
from PyQt6.QtGui import QIcon, QStandardItem

class ItemNode(QStandardItem):

    def __init__(self) -> None:
        super().__init__()
        self._q_icon = None
        self.setIcon(self.q_icon)
    
    @property
    def q_icon(self) -> QIcon:
        if self._q_icon is None:
            self._q_icon = QIcon()
        return self._q_icon

    @q_icon.setter
    def q_icon(self, icon: QIcon) -> None:
        self._q_icon = icon