from typing import List
from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsScene


class ItemGroup(object):

    def __init__(self) -> None:
        super().__init__()
        self.items: List[QGraphicsItem] = []
        self._bounding_rect = QRectF()
        self._z_value = 0

    def __calculate_rect(self):
        self._bounding_rect = QRectF()
        for item in self.items:
            self._bounding_rect = self._bounding_rect.united(item.sceneBoundingRect())

    def add_to_group(self, item: QGraphicsItem):
        self.items.append(item)
        self.__calculate_rect()

    def remove_from_group(self, item: QGraphicsItem):
        self.items.remove(item)
        item.scene().removeItem(item)
        self.__calculate_rect()

    def recalculate_rect(self):
        self.__calculate_rect()

    def child_items(self):
        return self.items

    def bounding_rect(self):
        return self._bounding_rect
    
    def set_z_value(self, value):
        self._z_value = value
        for item in self.items:
            item.setZValue(self._z_value)

    def get_z_value(self):
        return self._z_value

    def enable_group(self, indicator):
        for item in self.items:
            item.setEnabled(indicator)
