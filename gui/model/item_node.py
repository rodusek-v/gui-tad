
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QIcon, QStandardItem

from model.helpers import TextModel


class Signaler(QObject):

    rename_signal = pyqtSignal()
    children_changed = pyqtSignal()
    container_chaged = pyqtSignal()


class ItemNode(QStandardItem, TextModel):

    def __init__(self) -> None:
        super().__init__()
        self._ref_count = 0
        self._q_icon = None

        self.template_path = f"template/{self.__class__.__name__.lower()}.template"
        self.setIcon(self.q_icon)
        self.setEditable(False)
        self.__signaler = Signaler()

    @property
    def ref_count(self) -> int:
        return self._ref_count

    @ref_count.setter
    def ref_count(self, value: int) -> None:
        self._ref_count = value
    
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

    @property
    def name(self) -> str:
        pass