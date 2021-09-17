from PyQt6.QtCore import QSize
from PyQt6.QtGui import QDropEvent
from PyQt6.QtWidgets import QAbstractItemView

from view.fields.basic_list import BasicList


class ContainsList(BasicList):

    def __init__(self, controller, has_model=True) -> None:
        super().__init__()
        self.controller = controller
        self.has_model = has_model

        self.setStyleSheet(self.list_style.format("none", "none"))
        self.setIconSize(QSize(50, 50))
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)

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