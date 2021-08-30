
from PyQt6 import QtGui
from utils import translate_children
from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtWidgets import QScrollArea, QScrollBar


stylesheet = """
 /* --------------------------------------- QScrollBar  -----------------------------------*/
QScrollBar:horizontal {
    background-color: rgba(255, 255, 255, 0);
    height: 12px;
    margin: 3px 0x 3px 0px;
}

QScrollBar::handle:horizontal {
    background-color: #878484; 
    min-width: 5px;
    border-radius: 3px;
}

QScrollBar::add-line:horizontal {
    background: none;
}

QScrollBar::sub-line:horizontal {
    background: none;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}

QScrollBar:vertical {
    background-color: rgba(255, 255, 255, 0);
    width: 12px;
    margin: 0px 3px 0px 3px;
}

QScrollBar::handle:vertical {
    background-color: #878484; 
    min-height: 5px;
    border-radius: 3px;
}

QScrollBar::sub-line:vertical {
    background: none;
}

QScrollBar::add-line:vertical {
    background: none;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
"""


class GridScrollBar(QScrollBar):

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setStyleSheet(stylesheet)


class GridScroll(QScrollArea):

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setVerticalScrollBar(GridScrollBar())
        self.setHorizontalScrollBar(GridScrollBar())
        self.last_time_move = (0, 0)
        self.pressed_coords = None
        self.grid = None

    def set_grid(self, grid):
        self.grid = grid
        self.setWidget(self.grid)

    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        if not self.grid.childrenRect().isEmpty():
            translate_children(self.grid, 0, a0.angleDelta().y() / 3)
            self.grid.resize_grid()
            if self.grid.check_children_visibility():
                self.repaint()
        return super().wheelEvent(a0)

    def eventFilter(self, source, event) -> bool:
        if not isinstance(source, GridScrollBar):
            if event.type() == QEvent.Type.MouseMove and event.buttons() == Qt.MouseButton.LeftButton:
                if self.pressed_coords == None:
                    self.pressed_coords = event.position()
                if self.last_time_move == (0, 0):
                    self.last_time_move = (event.position().x(), event.position().y())

                distance_h = self.last_time_move[1] - event.position().y()
                distance_w = self.last_time_move[0] - event.position().x()
                
                x = self.pressed_coords.x()
                y = self.pressed_coords.y()
                dist_x = x - event.position().x()
                dist_y = y - event.position().y()

                if not self.grid.childrenRect().isEmpty():
                    translate_children(self.grid, -dist_x, -dist_y)
                    self.grid.resize_grid()
                    if self.grid.check_children_visibility():
                        self.repaint()
                        
                self.verticalScrollBar().setValue(self.verticalScrollBar().value() + distance_h)
                self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + distance_w)
                
                self.pressed_coords = event.position()
            elif event.type() == QEvent.Type.MouseButtonRelease:
                self.last_time_move = (0, 0)
                self.pressed_coords = None
        return super().eventFilter(source, event)
