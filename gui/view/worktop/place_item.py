from enum import Enum
from PyQt6.QtWidgets import QWidget

class Sides(Enum):
    N = "N"
    S = "S"
    W = "W"
    E = "E"

class PlaceItem(QWidget):

    inverse_side = {"N": "S", "S": "N", "E": "W", "W": "E"}

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self._neighbours = {
            key.name: None for key in Sides
        }

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

    def say_goodbye(self):
        for side, neighbour in self._neighbours.items():
            if neighbour:
                self.remove_neighbour(Sides(side))
                neighbour.remove_neighbour(Sides(self.inverse_side[side]))

    def __str__(self) -> str:
        return str(self.geometry().topLeft())