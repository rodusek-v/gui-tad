from model.item_node import ItemNode

class Finish(ItemNode):

    def __init__(
        self,
        position=None,
        flag=None
    ) -> None:
        super().__init__()
        self.position = position
        self.flag = flag