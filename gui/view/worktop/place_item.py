from enum import Enum
from PyQt6.QtCore import QPointF, QRectF, QSizeF
from PyQt6.QtWidgets import QWidget

class Sides(Enum):
    N = "N"
    S = "S"
    W = "W"
    E = "E"

class PlaceItem(QWidget):

    inverse_side = {"N": "S", "S": "N", "E": "W", "W": "E"}
    directions = {
        "N": QPointF(0, -1), "E": QPointF(1, 0), 
        "S": QPointF(0, 1), "W": QPointF(-1, 0)
    }

    def __init__(self, model, parent=None, margin=10, cwidth=10) -> None:
        super().__init__(parent=parent)
        self._neighbours = {
            key.name: None for key in Sides
        }
        self.margin = margin
        self.cwidth = cwidth
        self.model = model

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

    @property
    def neighbours(self):
        return self._neighbours

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
            if neighbour:
                self.remove_neighbour(Sides(side))
                neighbour.remove_neighbour(Sides(self.inverse_side[side]))
                rel_rect = self.__relation_rect(Sides(side))
                rel_centers.append(QPointF(
                    rel_rect.x() + rel_rect.width() / 2,
                    rel_rect.y() + rel_rect.height() / 2,
                ))
        return rel_centers
