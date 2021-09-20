from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

from view.buttons import ToggleButton


class MessageBox(QMessageBox):

    def __init__(self, parent, name: str):
        super().__init__(parent=parent)
        font = self.parent().font()
        font.setPointSize(12)
        self.setFont(font)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("""
            QMessageBox {
                background: #262626;
            }
            QMessageBox QLabel { 
                color: #bfbfbf;
            }
            QMessageBox QPushButton {
                background: #c3c3e3;
                padding: 5px 10px 5px 10px;
                border: none;
            }
            QMessageBox QPushButton:hover {
                background: #8c8ca3
            }
        """)
        self.setIcon(self.Icon.Warning)
        ok_button = ToggleButton("Close")
        ok_button.setStyle("color", "#bfbfbf")
        ok_button.setFixedWidth(60)
        ok_button.setCheckable(False)
        self.setStandardButtons(self.StandardButton.Close)
        self.setText(f"""
            Sorry, <strong>{name}</strong> can't be deleted
            <br/>
            due to its existance in other items.
        """)