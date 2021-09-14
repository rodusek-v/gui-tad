from model.item_node import ItemNode

class Flag(ItemNode):

    def __init__(
        self,
        name=None,
        activated=None,
        action_on_true=None,
        action_on_false=None
    ) -> None:
        super().__init__()
        self.name = name
        self.activated = activated
        self.action_on_true = action_on_true
        self.action_on_false = action_on_false