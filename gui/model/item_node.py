
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QIcon, QStandardItem


class Signaler(QObject):

    rename_signal = pyqtSignal()
    children_changed = pyqtSignal()
    container_chaged = pyqtSignal()


class ItemNode(QStandardItem):

    def __init__(self) -> None:
        super().__init__()
        self._q_icon = None
        self.setIcon(self.q_icon)
        self.__signaler = Signaler()
    
    @property
    def q_icon(self) -> QIcon:
        if self._q_icon is None:
            self._q_icon = QIcon()
        return self._q_icon

    @q_icon.setter
    def q_icon(self, icon: QIcon) -> None:
        self._q_icon = icon

    @property
    def rename_signal(self) -> pyqtSignal:
        return self.__signaler.rename_signal

    @property
    def children_changed(self) -> pyqtSignal:
        return self.__signaler.children_changed

    @property
    def container_chaged(self) -> pyqtSignal:
        return self.__signaler.container_chaged