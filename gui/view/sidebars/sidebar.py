from PyQt6.QtCore import QObject, QRect
from PyQt6.QtWidgets import QHBoxLayout, QWidget


class SideBar(QObject):

    def __init__(self, parent=None) -> None:
        super().__init__()    
        self._holder = QWidget(parent=parent)
        self.widget = None
        self._holder.setLayout(QHBoxLayout())
        self._holder.setStyleSheet("background-color: rgb(140, 140, 140);")
        self._holder.resize(0, 0)

    @property
    def holder(self):
        return self._holder

    def width(self):
        return self.holder.width()

    def setGeometry(self, rect: QRect):
        self.holder.setGeometry(rect)

    def setGeometry(self, x: int, y: int, width: int, height: int):
        self.holder.setGeometry(x, y, width, height)

    def set_form(self, model):
        pass