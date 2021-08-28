import math
from PyQt6.QtCore import QEvent, QPoint, Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QScrollArea, QScrollBar, QWidget


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

    def eventFilter(self, source, event) -> bool:
        if event.type() == QEvent.Type.Wheel:
            size = self.widget().size()
            if GridScroll.is_scrollbar_resizable(self.verticalScrollBar()):
                size.setHeight(size.height() + 20)
                self.__translate_children(0, GridScroll.sign_increase_value(self.verticalScrollBar(), 20))
                self.widget().resize(size)
        if isinstance(source, GridScrollBar) and event.type() == QEvent.Type.MouseMove \
             and event.buttons() == Qt.MouseButton.LeftButton:
            size = self.widget().size()
            if GridScroll.is_scrollbar_resizable(source):
                if self.horizontalScrollBar() == source:
                    size.setWidth(size.width() + 2)
                    self.__translate_children(GridScroll.sign_increase_value(source, 2), 0)
                    self.widget().resize(size)
                else:
                    size.setHeight(size.height() + 2)
                    self.__translate_children(0, GridScroll.sign_increase_value(source, 2))
                    self.widget().resize(size)
        if not isinstance(source, GridScrollBar):
            if event.type() == QEvent.Type.MouseMove and event.buttons() == Qt.MouseButton.LeftButton:
                if self.pressed_coords == None:
                    self.pressed_coords = event.position()
                if self.last_time_move == (0, 0):
                    self.last_time_move = (event.position().x(), event.position().y())

                distance_h = self.last_time_move[1] - event.position().y()
                distance_w = self.last_time_move[0] - event.position().x()

                size = self.widget().size()
                x = self.pressed_coords.x()
                y = self.pressed_coords.y()
                dist_x = x - event.position().x()
                dist_y = y - event.position().y()

                if GridScroll.is_scrollbar_resizable(self.verticalScrollBar()):
                    size.setHeight(size.height() + abs(dist_y))
                    self.last_time_move = (event.position().x(), event.position().y())
                    
                if GridScroll.is_scrollbar_resizable(self.horizontalScrollBar()):
                    size.setWidth(size.width() + abs(dist_x))
                    self.last_time_move = (event.position().x(), event.position().y())

                self.widget().resize(size)
                self.__translate_children(-dist_x, -dist_y)
                
                self.verticalScrollBar().setValue(self.verticalScrollBar().value() + distance_h)
                self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + distance_w)
                
                self.pressed_coords = event.position()
                
            elif event.type() == QEvent.Type.MouseButtonRelease:
                self.last_time_move = (0, 0)
                self.pressed_coords = None
        return super().eventFilter(source, event)

    def __translate_children(self, value_x, value_y):
        for child in self.widget().children():
            geometry = child.geometry()
            geometry.translate(value_x, value_y)
            child.setGeometry(geometry)

    @staticmethod
    def is_scrollbar_resizable(scrollbar):
        return scrollbar.value() in \
                [scrollbar.minimum(), scrollbar.maximum()]  or \
                not scrollbar.isVisible()

    @staticmethod
    def sign_increase_value(scrollbar, val):
        if scrollbar.maximum() == scrollbar.value():
            return -val
        elif scrollbar.minimum() == scrollbar.value():
            return val