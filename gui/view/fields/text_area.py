from PyQt6.QtGui import QColor
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QPlainTextEdit

from view.worktop import GridScrollBar


class TextArea(QPlainTextEdit):

    text_modified = pyqtSignal(str)

    def __init__(self, text: str = None, parent = None):
        super().__init__(parent=parent)
        self.setPlainText(text)
        self.setStyleSheet("""
            QPlainTextEdit {
                border: 2px solid #545454;
            }
            QPlainTextEdit:hover {
                border: 2px solid #545454;
            }
            QPlainTextEdit:focus {
                border: 2px solid #b0b0b0;
            }
        """)
        self.textChanged.connect(lambda: self.text_modified.emit(self.toPlainText()))
        self.setVerticalScrollBar(GridScrollBar(vertical_color=QColor("#bfbfbf")))

