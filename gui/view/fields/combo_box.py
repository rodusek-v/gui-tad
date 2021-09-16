from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QComboBox

from view.worktop import GridScrollBar


class ComboBox(QComboBox):

    def __init__(self, parent = None) -> None:
        super().__init__(parent=parent)
        self.setStyleSheet("""
            QComboBox {
                padding: 1px 5px 5px 2px;
                border: 2px solid #545454;
            }
            QComboBox QAbstractItemView {
                outline: 0;
            }
            QComboBox QAbstractItemView::item {
                height: 20px; 
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #363636;
                border: none;
            }
        """)
        self.view().setVerticalScrollBar(GridScrollBar(vertical_color=QColor("#bfbfbf")))

    def setCurrentText(self, text: str) -> None:
        if text is None:
            text = ""
        super().setCurrentText(text)