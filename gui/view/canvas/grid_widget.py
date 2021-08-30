from PyQt6 import QtGui
from view.canvas.grid_scroll import GridScroll
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QWidget

class Grid(QFrame):

    def __init__(self) -> None:
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.grid_scroll = GridScroll(self)
        self.grid_scroll.setStyleSheet("background-color: #c9c5c5; border: none;")
        self.layout().setContentsMargins(0, 0, 0, 0)
        
        self.canvas = CanvasGrid(self.grid_scroll)
        self.__trigger_bars()
        self.canvas.setStyleSheet("background-color: white")
        self.grid_scroll.set_grid(self.canvas)
        
        self.layout().addWidget(self.grid_scroll)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.__trigger_bars()
        return super().resizeEvent(a0)

    def __trigger_bars(self):
        height = self.grid_scroll.frameGeometry().height()
        width = self.grid_scroll.frameGeometry().width()
        size = self.canvas.size()
        if self.canvas.size().width() <= width:
            size.setWidth(width)
        
        if self.canvas.size().height() <= height:
            size.setHeight(height)

        self.canvas.resize(size)


class CanvasGrid(QFrame):

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        
    def get_current_rect(self):
        return self.childrenRect().united(self.visibleRegion().boundingRect())

    def check_children_visibility(self):
        for child in self.children():
            if child.visibleRegion().boundingRect().size() != child.size():
                return False
        return True

    def resize_grid(self):
        self.resize(self.get_current_rect().size())

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        t = QWidget()
        a = a0.position()
        t.setGeometry(a.x(), a.y(), 200, 200)
        t.setStyleSheet("background: blue;")
        t.setParent(self)
        t.show()
        return super().mouseDoubleClickEvent(a0)
    