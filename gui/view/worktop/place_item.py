from enum import Enum
from time import time

from PyQt6.QtCore import QItemSelection, QPointF, QRectF, QSize, QSizeF, Qt, pyqtSignal
from PyQt6.QtGui import QDropEvent, QKeyEvent, QMouseEvent
from PyQt6.QtWidgets import QAbstractItemView, QLabel, QListWidget

from view.worktop.object_item import ObjectItem
from model.place import Place, Object
from controller import PlaceController

class Sides(Enum):
    N = "N"
    S = "S"
    W = "W"
    E = "E"

class Title(QLabel):

    def __init__(self, parent: 'PlaceItem') -> None:
        super().__init__(parent)
        self._parent = parent
        self.click_interval = -1

    def __double_click(self):
        if self.click_interval == -1:
            self.click_interval = time()
        else:
            now = time()
            diff = now - self.click_interval
            if diff <= 0.2:
                return True
            self.click_interval = now

        return False

    def mousePressEvent(self, event) -> None:
        self._parent.clearSelection()
        if self.__double_click():
            self._parent.selected_place.emit(self._parent.place_model)
        super().mousePressEvent(event)

class PlaceItem(QListWidget):

    selected_object = pyqtSignal(Object)
    selected_place = pyqtSignal(Place)
    removed_object = pyqtSignal(Object)
    removed_place = pyqtSignal()
    current_item = pyqtSignal(Object)

    inverse_side = {"N": "S", "S": "N", "E": "W", "W": "E"}
    directions = {
        "N": QPointF(0, -1), "E": QPointF(1, 0), 
        "S": QPointF(0, 1), "W": QPointF(-1, 0)
    }

    def __init__(self, model: 'Place', parent=None, margin=10, size=100) -> None:
        super().__init__(parent=parent)
        self._neighbours = {
            key.name: None for key in Sides
        }
        self.margin = margin
        self.cwidth = size * 0.1
        self._model = model
        self._model.rename_signal.connect(self.__set_title)
        self._model.container_changed.connect(self.__fill_item)
        self.controller = PlaceController(self._model)
        self.click_interval = -1

        self.setStyleSheet("""
            QListWidget {
                outline: 0;
            }
            :enabled {
                background: rgb(140, 140, 140);
                color: black;
            }
            :disabled {
                background: rgb(140, 140, 140);
                color: black;
            }
            :item {
                margin: 0px;
                padding: 0px;
                border: none;
            }
            :item::selected {
                background-color: rgba(61, 61, 61, 0.7);
            }
        """)

        self.label = Title(self)
        self.label.resize(size, self.label.height())
        font = self.label.font()
        font.setPointSize(8)
        self.label.setFont(font)
        self.__set_title()
        self.setContentsMargins(0, 0, 0, 0)
        self.setViewportMargins(0, self.label.height(), 0, 0)

        self.setAcceptDrops(True)
        self.setIconSize(QSize(size / 3.5, size / 3.5))
        self.setGridSize(QSize(size / 3.5, size / 3.5))
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.setResizeMode(self.ResizeMode.Adjust)
        self.setViewMode(self.ViewMode.IconMode)
        self.setSelectionMode(self.SelectionMode.ExtendedSelection)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.__fill_item()
        self.setEnabled(False)

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
        self.clear()
        for obj in self._model.contains:
            self.add_object(obj)

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

    def __double_click(self):
        if self.click_interval == -1:
            self.click_interval = time()
        else:
            now = time()
            diff = now - self.click_interval
            if diff <= 0.2:
                return True
            self.click_interval = now

        return False

    def dropEvent(self, event: QDropEvent) -> None:
        if self != event.source() and isinstance(event.source(), PlaceItem):
            #super().dropEvent(event)
            source = event.source()
            objects_to_move = []
            for i in range(len(source.selectedIndexes()) - 1, -1, -1):
                item = source.takeItem(source.selectedIndexes()[i].row())
                objects_to_move.append(item)
                self.addItem(item)
            self.controller.assign_objects([obj.model for obj in objects_to_move])
            source.clearSelection()
        else:
            event.ignore()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        double_click = self.__double_click()
        item = self.itemAt(event.position().toPoint())
        if double_click:
            if item is not None:
                self.selected_object.emit(item.model)
            else:
                self.selected_place.emit(self.place_model)
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        item = self.itemAt(event.position().toPoint())
        selected_indexes = len(self.selectedIndexes())
        if item is not None and selected_indexes == 1:
            self.current_item.emit(item.model)
        return super().mouseReleaseEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            if len(self.selectedIndexes()) == 1:
                self.remove_selected()
            elif len(self.selectedIndexes()) == 0:
                self.removed_place.emit()
        else:
            super().keyPressEvent(event)

    @property
    def neighbours(self):
        return self._neighbours

    @property
    def title(self):
        return self._model.name

    @property
    def place_model(self):
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

    def select_item(self, model):
        for i in range(self.count()):
            if self.item(i).model == model:
                self.setCurrentItem(self.item(i))
                break

    def add_object(self, object):
        object_item = ObjectItem(object, self)
        self.addItem(object_item)

    def remove_selected(self):
        if len(self.selectedIndexes()) != 0:
            item = self.takeItem(self.selectedIndexes()[0].row())
            self.removed_object.emit(item.model)

    def setGeometry(self, rect: QRectF) -> None:
        super().setGeometry(rect)
        self.place_model.position = rect
