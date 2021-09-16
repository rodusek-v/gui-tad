from PyQt6.QtWidgets import QCheckBox


class CheckBox(QCheckBox):

    def __init__(self, text: str = None, parent = None):
        super().__init__(parent=parent)
        if text:
            self.setText(text)

        self.setStyleSheet("""
            QCheckBox::indicator {
                width: 25px;
                height: 25px;
                background-color: #bfbfbf;
            }
            QCheckBox::indicator:checked {
                image: url(icons/check.png);
            }
            QCheckBox::indicator:checked:hover {
                image: url(icons/check_hover.png);
            }
            QCheckBox::indicator:unchecked:hover {
                image: url(icons/uncheck_hover.png);
            }
        """)