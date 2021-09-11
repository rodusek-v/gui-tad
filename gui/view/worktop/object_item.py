from PyQt6.QtWidgets import QListWidgetItem

class ObjectItem(QListWidgetItem):

    def __init__(self, model, parent=None) -> None:
        super().__init__(parent=parent)
        self._model = model
        self.setIcon(self._model.icon())
