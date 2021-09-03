from PyQt6.QtWidgets import QScrollBar

stylesheet = """
 /* --------------------------------------- QScrollBar  -----------------------------------*/
QScrollBar:horizontal {
    background-color: transparent;
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
    background-color: transparent;
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

    def move_scroll_bar(self, d):
        self.setValue(self.value() + d)

    def is_min_max_same(self):
        return self.minimum() == self.maximum()

    def is_at_maximum(self):
        return self.value() == self.maximum()

    def is_at_minimum(self):
        return self.value() == self.minimum()