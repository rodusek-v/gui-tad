from PyQt6.QtGui import QIcon

from model.utils import Action
from model.item_node import ItemNode


class Flag(ItemNode):

    def __init__(
        self,
        name: str = "",
        activated: bool = False,
    ) -> None:
        super().__init__()
        self.name = name
        self.activated = activated
        self.action_on_true = Action()
        self.action_on_false = Action()

    @property
    def q_icon(self) -> QIcon:
        if self._q_icon is None:
            icon = QIcon()
            icon.addFile("icons/nodes/flag.png", mode=QIcon.Mode.Active)
            icon.addFile("icons/nodes/flag.png", mode=QIcon.Mode.Selected)
            icon.addFile("icons/nodes/flag.png", mode=QIcon.Mode.Disabled)
            self._q_icon = icon
        return self._q_icon

    @q_icon.setter
    def q_icon(self, icon: QIcon) -> None:
        self._q_icon = icon

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value
        self.setText(self._name)

    @property
    def activated(self) -> bool:
        return self._activated

    @activated.setter
    def activated(self, value: bool) -> None:
        self._activated = value

    @property
    def action_on_true(self) -> Action:
        return self._action_on_true

    @action_on_true.setter
    def action_on_true(self, value: Action) -> None:
        self._action_on_true = value

    @property
    def action_on_false(self) -> Action:
        return self._action_on_false

    @action_on_false.setter
    def action_on_false(self, value: Action) -> None:
        self._action_on_false = value

    def serialize(self):
        ser = dict(self.__dict__)
        del ser['_q_icon']
        del ser['_ItemNode__signaler']
        del ser['_ref_count']
        del ser['template_path']
        ser['_action_on_true'] = self.action_on_true.serialize()
        ser['_action_on_false'] = self.action_on_false.serialize()
        return ser

    def load(self, serialized):
        self.name = serialized['_name']
        self.action_on_true.message = serialized['_action_on_true']['message']
        self.action_on_false.message = serialized['_action_on_false']['message']