from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QMouseEvent
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


    def eventFilter(self, source, event) -> bool:
        if not isinstance(source, GridScrollBar):
            if event.type() == QEvent.Type.MouseMove:
                if self.last_time_move == (0, 0):
                    self.last_time_move = (event.position().x(), event.position().y())

                distance = self.last_time_move[1] - event.position().y()
                self.verticalScrollBar().setValue(self.verticalScrollBar().value() + distance)
                distance = self.last_time_move[0] - event.position().x()
                self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + distance)
                
            elif event.type() == QEvent.Type.MouseButtonRelease:
                self.last_time_move = (0, 0)
        return super().eventFilter(source, event)