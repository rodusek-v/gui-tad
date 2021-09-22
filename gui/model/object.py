from typing import List
from PyQt6.QtGui import QIcon

from model.container import Container
from model.item_node import ItemNode


class Object(ItemNode, Container):

    def __init__(
        self,
        name: str = "new_object",
        description: 'Description' = None,
        contains: List['Object'] = None,
        pickable: bool = True,
        container: 'Container' = None
    ) -> None:
        super().__init__()
        self.name = name
        if description is None:
            description = Description()
        self.description = description
        if contains is None:
            contains = []
        self.contains = contains
        self.pickable = pickable
        self.container = container

    @property
    def q_icon(self) -> QIcon:
        if self._q_icon is None:
            icon = QIcon()
            icon.addFile("icons/nodes/object.png", mode=QIcon.Mode.Active)
            icon.addFile("icons/nodes/object.png", mode=QIcon.Mode.Selected)
            icon.addFile("icons/nodes/object.png", mode=QIcon.Mode.Disabled)
            self._q_icon = icon
        return self._q_icon

    @q_icon.setter
    def q_icon(self, icon: QIcon) -> None:
        self._q_icon = icon

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value
        self.setText(self._name)

    @property
    def description(self) -> 'Description':
        return self._description

    @description.setter
    def description(self, value: 'Description'):
        self._description = value

    @property
    def contains(self) -> List['Object']:
        return self._contains

    @contains.setter
    def contains(self, value: List['Object']):
        self._contains = value

    @property
    def pickable(self) -> bool:
        return self._pickable

    @pickable.setter
    def pickable(self, value: bool):
        self._pickable = value

    @property
    def container(self) -> 'Container':
        return self._container

    @container.setter
    def container(self, value: 'Container'):
        self._container = value
        self.container_chaged.emit()

    @container.deleter
    def container(self):
        self._container = None
        self.container_chaged.emit()

    def serialize(self):
        ser = dict(self.__dict__)
        del ser['_q_icon']
        del ser['_ItemNode__signaler']
        del ser['_ref_count']
        del ser['template_path']
        ser['_description'] = self.description.__dict__
        ser['_contains'] = [obj.name for obj in self.contains]
        ser['_container'] = None if self.container is None else self.container.name
        return ser

    def load(self, serialized):
        self.name = serialized['_name']
        self.description.name = serialized['_description']['name']
        self.description.description = serialized['_description']['description']

    def add_object(self, object: 'Object') -> None:
        object.container = self
        self._contains.append(object)

    def get_objects(self) -> List['Object']:
        return self.contains

    def remove_object(self, object: 'Object') -> None:
        try:
            self.contains.remove(object)
            del object.container
        except ValueError:
            pass


from model.utils import Description