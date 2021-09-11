from enum import Enum
from PyQt6.QtCore import QPointF, QRectF, QSize, QSizeF, Qt
from PyQt6.QtGui import QDropEvent
from PyQt6.QtWidgets import QAbstractItemView, QLabel, QListWidget, QSizePolicy

from view.worktop.object_item import ObjectItem

class Sides(Enum):
    N = "N"
    S = "S"
    W = "W"
    E = "E"

class PlaceItem(QListWidget):

    inverse_side = {"N": "S", "S": "N", "E": "W", "W": "E"}
    directions = {
        "N": QPointF(0, -1), "E": QPointF(1, 0), 
        "S": QPointF(0, 1), "W": QPointF(-1, 0)
    }

    def __init__(self, model, parent=None, margin=10, cwidth=10, size=100) -> None:
        super().__init__(parent=parent)
        self._neighbours = {
            key.name: None for key in Sides
        }
        self.margin = margin
        self.cwidth = cwidth
        self._model = model

        self.label = QLabel(self)
        self.label.resize(size, self.label.height())
        font = self.label.font()
        font.setPointSize(8)
        self.label.setFont(font)
        self.__set_title()
        self.setViewportMargins(0, self.label.height(), 0, 0)

        self.setAcceptDrops(True)
        self.setIconSize(QSize(size / 4.54, size / 4.54))
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.setResizeMode(self.ResizeMode.Adjust)
        self.setViewMode(self.ViewMode.IconMode)
        self.setSelectionMode(self.SelectionMode.ExtendedSelection)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.__fill_item()
    
    def __set_title(self):
        text = self._model.name
        title_size = len(text) * self.label.font().pointSize()
        width = self.label.width()
        if title_size > width + self.label.font().pointSize():
            temp = int(width / self.label.font().pointSize()) + 1
            text = text[:temp - 3] + "..."
        self.label.setText(text)
        self.label.setContentsMargins(10, 0, 0, 0)
        self.label.setStyleSheet("border-bottom: 1px solid black;")
    
    def __fill_item(self):
        for obj in self._model.contains:
            self.list_model.appendRow(obj)

    def __relation_rect(self, side: Sides):
        geometry = self.geometry()
        if side == Sides.N:
            point = QPointF(
                geometry.x() + geometry.width() / 2 - self.cwidth / 2,
                geometry.y() - self.margin * 2 - self.cwidth / 2,
            )
            size = QSizeF(self.cwidth, self.margin * 2 + self.cwidth)
        elif side == Sides.S:
            point = QPointF(
                geometry.bottomLeft().x() + geometry.width() / 2 - self.cwidth / 2,
                geometry.bottomLeft().y() - self.cwidth / 2,
            )
            size = QSizeF(self.cwidth, self.margin * 2 + self.cwidth)
        elif side == Sides.W:
            point = QPointF(
                geometry.x() - self.margin * 2 - self.cwidth / 2,
                geometry.y() + geometry.height() / 2,
            )
            size = QSizeF(self.margin * 2 + self.cwidth, self.cwidth)
        elif side == Sides.E:
            point = QPointF(
                geometry.topRight().x() - self.cwidth / 2,
                geometry.topRight().y() + geometry.height() / 2,
            )
            size = QSizeF(self.margin * 2 + self.cwidth, self.cwidth)

        return QRectF(point, size)

    def dropEvent(self, event: QDropEvent) -> None:
        if self != event.source():
            super().dropEvent(event)
            source = event.source()
            for i in range(len(source.selectedIndexes()) - 1, -1, -1):
                source.takeItem(source.selectedIndexes()[i].row())
            source.clearSelection()
        else:
            event.ignore()

    @property
    def neighbours(self):
        return self._neighbours

    @property
    def title(self):
        return self._model.name

    @property
    def model(self):
        return self._model

    def set_neighbour(self, side: Sides, neighbour):
        self._neighbours[side.name] = neighbour

    def check_if_neighbour_exist(self, side: Sides):
        return self._neighbours[side.name] is not None

    def remove_neighbour(self, side: Sides):
        self._neighbours[side.name] = None

    def say_hello(self, side: Sides, neighbour):
        self.set_neighbour(side, neighbour)
        self._neighbours[side.name].set_neighbour(
            Sides(self.inverse_side[side.name]), self)

        return self.__relation_rect(side)

    def say_goodbye(self):
        rel_centers = []
        for side, neighbour in self._neighbours.items():
            if neighbour is not None:
                self.remove_neighbour(Sides(side))
                neighbour.remove_neighbour(Sides(self.inverse_side[side]))
                rel_rect = self.__relation_rect(Sides(side))
                rel_centers.append(QPointF(
                    rel_rect.x() + rel_rect.width() / 2,
                    rel_rect.y() + rel_rect.height() / 2,
                ))

        return rel_centers

    def add_object(self, object):
        object_item = ObjectItem(object, self)
        self.addItem(object_item)
        #print(self.item(self.count() - 1).listWidget())
