from PyQt6.QtCore import QSize
from PyQt6.QtGui import QColor, QDropEvent
from PyQt6.QtWidgets import QAbstractItemView, QListWidget

from view.worktop import GridScrollBar


class ContainsList(QListWidget):

    def __init__(self, controller, has_model=True) -> None:
        super().__init__()

        list_style = """
            QListWidget {
                outline: 0;
            }
            :enabled {
                background: transparent;
                color: #bfbfbf;
                border: none;
            }
            :item {
                margin: 0px;
                padding: 0px;
                border: none;
                border-bottom: 1px solid #545454;
            }
            :item::selected {
                background-color: rgba(61, 61, 61, 0.7);
            }
        """
        self.controller = controller
        self.has_model = has_model

        self.setStyleSheet(list_style)
        self.setIconSize(QSize(50, 50))
        self.setVerticalScrollBar(GridScrollBar(vertical_color=QColor("#bfbfbf")))
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.setResizeMode(self.ResizeMode.Adjust)
        self.setSelectionMode(self.SelectionMode.ExtendedSelection)

    def dropEvent(self, event: QDropEvent) -> None:
        if self != event.source() and isinstance(event.source(), ContainsList):
            source = event.source()
            objects_to_move = []
            for i in range(len(source.selectedIndexes()) - 1, -1, -1):
                item = source.takeItem(source.selectedIndexes()[i].row())
                objects_to_move.append(item)
                self.addItem(item)
            if self.has_model:
                self.controller.assign_objects([obj.model for obj in objects_to_move])
            else:
                self.controller.free_objects([obj.model for obj in objects_to_move])
            source.clearSelection()
        else:
            event.ignore()