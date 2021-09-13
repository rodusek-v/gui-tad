from PyQt6.QtGui import QKeyEvent
from model.place import Place

from PyQt6.QtCore import QItemSelection, Qt, pyqtSignal
from PyQt6.QtWidgets import QTreeView

class WorldTreeView(QTreeView):

    selected_place = pyqtSignal(Place)
    remove_place_signal = pyqtSignal()
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setStyleSheet("border: none; background-color: transparent; color: #bfbfbf;")

    def selectionChanged(self, selected: QItemSelection, deselected: QItemSelection) -> None:
        for i in selected.indexes():
            item = self.model().itemFromIndex(i)
            if isinstance(item, Place):
                self.selected_place.emit(item)
        return super().selectionChanged(selected, deselected)
    
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            item = self.model().itemFromIndex(self.currentIndex())
            if isinstance(item, Place):
                self.remove_place_signal.emit()
        return super().keyPressEvent(event)

    def activate_selection(self):
        self.setSelectionMode(self.SelectionMode.SingleSelection)

    def deactivate_selection(self):
        self.setSelectionMode(self.SelectionMode.NoSelection)
        