from PyQt6.QtGui import QColor, QKeyEvent, QMouseEvent
from PyQt6.QtCore import QItemSelection, Qt, pyqtSignal
from PyQt6.QtWidgets import QTreeView

from view.worktop import GridScrollBar
from model import Place, Object, Flag, ItemNode

class WorldTreeView(QTreeView):

    selected_place = pyqtSignal(Place)
    selected_object = pyqtSignal(Object)
    remove_place_signal = pyqtSignal()
    remove_flag_signal = pyqtSignal(Flag)
    remove_container_object_signal = pyqtSignal(Place)
    remove_object_signal = pyqtSignal(Object)
    selected_item = pyqtSignal(ItemNode)
    deselect = pyqtSignal()
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setStyleSheet("""
            QTreeView {
                border: none; 
                background-color: transparent; 
                color: #bfbfbf;
                outline: 0;
            }
            :item {
                border: none;
            }
            :item::selected {
                background-color: rgb(61, 61, 61);
            }
            :item::hover {
                background-color: rgb(70, 70, 70);
            }
        """)
        self.setVerticalScrollBar(GridScrollBar(vertical_color=QColor("#bfbfbf")))
        self.setHorizontalScrollBar(GridScrollBar(vertical_color=QColor("#bfbfbf")))

    def selectionChanged(self, selected: QItemSelection, deselected: QItemSelection) -> None:
        for i in selected.indexes():
            item = self.model().itemFromIndex(i)
            if isinstance(item, Place):
                self.selected_place.emit(item)
            elif isinstance(item, Object):
                if isinstance(item.container, Place):
                    self.selected_object.emit(item)
            elif isinstance(item, Flag):
                pass
            else:
                self.deselect.emit()
        return super().selectionChanged(selected, deselected)
    
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            item = self.model().itemFromIndex(self.currentIndex())
            if isinstance(item, Place):
                self.remove_place_signal.emit()
            elif isinstance(item, Object):
                if isinstance(item.container, Place):
                    self.remove_container_object_signal.emit(item.container)
                elif item.container is None:
                    self.remove_object_signal.emit(item)
            elif isinstance(item, Flag):
                self.remove_flag_signal.emit(item)
                self.clearSelection()
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
        