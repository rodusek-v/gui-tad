from PyQt6.QtGui import QAction, QColor, QKeyEvent, QMouseEvent, QStandardItem
from PyQt6.QtCore import QItemSelection, Qt, pyqtSignal
from PyQt6.QtWidgets import QMenu, QTreeView

from view.worktop import GridScrollBar
from model import Place, Object, Flag, ItemNode, Command

class WorldTreeView(QTreeView):

    selected_place = pyqtSignal(Place)
    selected_object = pyqtSignal(Object)
    remove_place_signal = pyqtSignal()
    remove_flag_signal = pyqtSignal(Flag)
    remove_command_signal = pyqtSignal(Command)
    remove_container_object_signal = pyqtSignal(Place)
    remove_object_signal = pyqtSignal(Object)
    selected_item = pyqtSignal(ItemNode)
    deselect = pyqtSignal()
    no_container_object = pyqtSignal()
    
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
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__open_context_menu)

        self.add_object = QAction("Add object")
        self.add_flag = QAction("Add flag")
        self.add_command = QAction("Add command")

    def __open_context_menu(self, position):
        indexes = self.selectedIndexes()
        if len(indexes) == 0:
            return

        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #262626;
                color: #bfbfbf;
            }
            QMenu::item::selected {
                background-color: #3d3d3d;
            }
        """)

        if len(indexes) == 1:
            item = self.model().itemFromIndex(indexes[0])
            if isinstance(item, ItemNode):
                edit = QAction("Edit")
                edit.triggered.connect(lambda: self.selected_item.emit(item))
                menu.addAction(edit)
                delete = QAction("Delete")
                delete.triggered.connect(self.__remove_item_signal)
                menu.addAction(delete)
            elif isinstance(item, QStandardItem):
                if item.text() == "Objects":
                    menu.addAction(self.add_object)
                elif item.text() == "Flags":
                    menu.addAction(self.add_flag)
                elif item.text() == "Commands":
                    menu.addAction(self.add_command)

        menu.exec(self.viewport().mapToGlobal(position))

    def __remove_item_signal(self):
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
        elif isinstance(item, Command):
            self.remove_command_signal.emit(item)

    def selectionChanged(self, selected: QItemSelection, deselected: QItemSelection) -> None:
        for i in selected.indexes():
            item = self.model().itemFromIndex(i)
            if isinstance(item, Place):
                self.selected_place.emit(item)
            elif isinstance(item, Object):
                if isinstance(item.container, Place):
                    self.selected_object.emit(item)
                else:
                    self.no_container_object.emit()
            elif isinstance(item, ItemNode):
                pass
            else:
                self.deselect.emit()
        return super().selectionChanged(selected, deselected)
    
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            self.__remove_item_signal()
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
        
        