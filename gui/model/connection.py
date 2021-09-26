from typing import List

from model.item_node import ItemNode
from model.place import Place
from model.utils import Sides


class Connection(ItemNode):

    def __init__(
        self,
        place_1: 'Place' = None,
        direction: Sides = None,
        place_2: 'Place' = None,
    ) -> None:
        super().__init__()
        self.place_1 = place_1
        self.direction = direction
        self.place_2 = place_2

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Connection):
            same_direction = self.place_1 == o.place_1 and self.place_2 == o.place_2
            opposite_direction = self.place_1 == o.place_2 and self.place_2 == o.place_1
            return same_direction or opposite_direction
        return super().__eq__(o)

    def __str__(self) -> str:
        return f"{self.place_1.name}, {self.direction}, {self.place_2.name}"
