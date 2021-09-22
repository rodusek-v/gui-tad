from model.item_node import ItemNode


class Finish(ItemNode):

    def __init__(
        self,
        position: 'Place' = None,
        flag: 'Flag' = None,
        value: bool = True
    ) -> None:
        super().__init__()
        self.position = position
        self.flag = flag
        self.value = value

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

    @property
    def value(self) -> bool:
        return self._value

    @value.setter
    def value(self, value: bool) -> None:
        self._value = value

    def serialize(self):
        ser = dict(self.__dict__)
        del ser['_q_icon']
        del ser['_ItemNode__signaler']
        del ser['_ref_count']
        del ser['template_path']
        ser['_position'] = self.position.name if self.position else None
        ser['_flag'] = self.flag.name if self.flag else None
        return ser


from model.place import Place
from model.flag import Flag