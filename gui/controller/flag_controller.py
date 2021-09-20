from PyQt6.QtCore import QObject

from model import Flag
from model.utils import Action, Dependency


class FlagController(QObject):

    def __init__(self, model: Flag) -> None:
        super().__init__()
        self._model = model

    @property
    def model(self) -> Flag:
        return self._model

    @model.setter
    def model(self, value: Flag) -> None:
        self._model = value

    def set_name(self, name: str) -> None:
        self.model.name = name

    def get_name(self) -> str:
        return self.model.name

    def set_activated(self, activated: bool) -> None:
        self.model.activated = activated

    def get_activated(self) -> bool:
        return self.model.activated

    def get_action(self, type: bool) -> Action:
        if type:
            return self.model.action_on_true
        else:
            return self.model.action_on_false

    def set_true_message(self, message: str) -> None:
        self.model.action_on_true.message = message

    def get_true_message(self) -> str:
        return self.model.action_on_true.message

    def set_false_message(self, message: str) -> None:
        self.model.action_on_false.message = message

    def get_false_message(self) -> str:
        return self.model.action_on_false.message

    def add_true_dependency(self, flag: Flag, value: bool) -> None:
        if self.model != flag:
            flag.ref_count += 1
        self.model.action_on_true.add_dependency(Dependency(flag, value))

    def add_false_dependency(self, flag: Flag, value: bool) -> None:
        if self.model != flag:
            flag.ref_count += 1
        self.model.action_on_false.add_dependency(Dependency(flag, value))

    def remove_true_dependency(self, dependency: Dependency) -> None:
        dependency.flag.ref_count -= 1
        self.model.action_on_true.remove_dependency(dependency)

    def remove_false_dependency(self, dependency: Dependency) -> None:
        dependency.flag.ref_count -= 1
        self.model.action_on_false.remove_dependency(dependency) 
            