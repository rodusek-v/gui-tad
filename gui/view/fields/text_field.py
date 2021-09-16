import re

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeyEvent, QRegularExpressionValidator
from PyQt6.QtWidgets import QLineEdit


class TextField(QLineEdit):

    editing_done = pyqtSignal(str)

    def __init__(self, contents: str = None, parent = None):
        super().__init__(parent=parent)
        self.setText(contents)
        self.current_value = self.text()
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid transparent;
                border-bottom: 2px solid #545454;
            }
            :hover {
                border-bottom: 2px solid #b0b0b0;
            }
            :focus {
                border-bottom: 2px solid #ffffff;
            }
        """)
        self.setTextMargins(1, 5, 5, 2)

        self.editingFinished.connect(self.__set_current_value)
        self.editingFinished.connect(self.clearFocus)
        self.editingFinished.connect(lambda: self.editing_done.emit(self.text()))

    def __set_current_value(self):
        self.current_value = self.text()

    def reject(self):
        self.setText(self.current_value)
        self.clearFocus()

    def setText(self, text: str) -> None:
        validator = self.validator()
        if isinstance(validator, QRegularExpressionValidator):
            step = 0
            regex = validator.regularExpression().pattern()
            while validator.validate(text, 0)[0] != validator.State.Acceptable:
                if step == 0:
                    text = "_".join(text.split())
                elif step == 1:
                    text = f"_{text}"
                else:
                    text = "".join(re.findall(regex, text))

                step += 1
        super().setText(text)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.reject()
        return super().keyPressEvent(event)
        