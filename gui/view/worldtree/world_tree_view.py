from PyQt6.QtGui import QColor, QKeyEvent, QMouseEvent
from PyQt6.QtCore import QItemSelection, Qt, pyqtSignal
from PyQt6.QtWidgets import QTreeView

from view.worktop import GridScrollBar
from model import Place, ItemNode

class WorldTreeView(QTreeView):

    selected_place = pyqtSignal(Place)
    remove_place_signal = pyqtSignal()
    selected_item = pyqtSignal(ItemNode)
    deselect = pyqtSignal()
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setStyleSheet("border: none; background-color: transparent; color: #bfbfbf;")
        self.setVerticalScrollBar(GridScrollBar(vertical_color=QColor("#bfbfbf")))

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
        elif event.key() == Qt.Key.Key_Escape:
            self.clearSelection()
            self.deselect.emit()
        return super().keyPressEvent(event)

    def mouseDoubleClickEvent(self, e: QMouseEvent) -> None:
        item = self.model().itemFromIndex(self.currentIndex())
        if isinstance(item, ItemNode):
            self.selected_item.emit(item)

        return super().mouseDoubleClickEvent(e)

    def activate_selection(self):
        self.setSelectionMode(self.SelectionMode.SingleSelection)

    def deactivate_selection(self):
        self.setSelectionMode(self.SelectionMode.NoSelection)
        