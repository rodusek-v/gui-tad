from PyQt6.QtWidgets import QPushButton, QSizePolicy
from PyQt6.QtCore import QEvent, QObject
from PyQt6.QtGui import QEnterEvent


class ToggleButton(QPushButton):
    def __init__(self, text: str = None, parent: QObject = None):
        super().__init__(text, parent)
        self.styles = {
            "border": "none",
            "padding": "10px",
            "margin": "0px",
            "background": "transparent"
        }
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.setStyleSheet(self.__get_style())
        self.setCheckable(True)

    def __get_style(self):
        return " ".join([f"{key}: {value};" for key, value in self.styles.items()])

    def select(self):
        if self.isChecked():
            self.styles["background"] = "#393f4f"
        else:
            self.styles["background"] = "transparent"
        self.setStyleSheet(self.__get_style())

    def enterEvent(self, event: QEnterEvent) -> None:
        if not self.isChecked():
            self.styles["background"] = "#363636"
            self.setStyleSheet(self.__get_style())
        return super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        if not self.isChecked():
            self.styles["background"] = "transparent"
            self.setStyleSheet(self.__get_style())
        return super().leaveEvent(event)

    def setStyle(self, key, value):
        self.styles[key] = value
        self.setStyleSheet(self.__get_style())
        self.repaint()

