
from PyQt6.QtWidgets import QWidget

class Form(QWidget):
    
    def __init__(self, model, parent=None) -> None:
        super().__init__(parent=parent)
        self._model = model

    @property
    def model(self):
        return self._model