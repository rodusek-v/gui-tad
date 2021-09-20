from model.item_node import ItemNode


class Finish(ItemNode):

    def __init__(
        self,
        position: 'Place' = None,
        flag: 'Flag' = None
    ) -> None:
        super().__init__()
        self.position = position
        self.flag = flag

    @property
    def position(self) -> 'Place':
        return self._position

    @position.setter
    def position(self, value: 'Place') -> None:
        self._position = value

    @property
    def flag(self) -> 'Flag':
        return self._flag

    @flag.setter
    def flag(self, value: 'Flag') -> None:
        self._flag = value


from model.place import Place
from model.flag import Flag