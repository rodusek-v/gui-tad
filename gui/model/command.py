from typing import Dict, List
from PyQt6.QtGui import QIcon

from model.operation import CDMOperation, CDMProp, FlagOperation, MessageOperation, Operation, RelocateOperation, Requirements
from model.item_node import ItemNode
from constants import THIS_FOLDER


class Command(ItemNode):

    def __init__(
        self,
        id: int,
        text: List[str] = None,
        operation: Operation = None
    ) -> None:
        super().__init__()
        self._id = id
        if text is None:
            text = []
        self.cmd_text = text
        self.operation = operation

    @property
    def q_icon(self) -> QIcon:
        if self._q_icon is None:
            icon = QIcon()
            png_path = "/".join([THIS_FOLDER, "icons/nodes/command.png"])
            icon.addFile(png_path, mode=QIcon.Mode.Active)
            icon.addFile(png_path, mode=QIcon.Mode.Selected)
            icon.addFile(png_path, mode=QIcon.Mode.Disabled)
            self._q_icon = icon
        return self._q_icon

    @q_icon.setter
    def q_icon(self, icon: QIcon) -> None:
        self._q_icon = icon

    @property
    def name(self) -> str:
        return str(self._id)

    @property
    def cmd_text(self) -> List[str]:
        return self._cmd_text

    @cmd_text.setter
    def cmd_text(self, value: List[str]) -> None:
        self._cmd_text = value
        self.setText(", ".join(self._cmd_text[:3]))

    @property
    def operation(self) -> Operation:
        return self._operation

    @operation.setter
    def operation(self, value: Operation) -> None:
        self._operation = value

    def serialize(self):
        ser = dict(self.__dict__)
        del ser['_q_icon']
        del ser['_ItemNode__signaler']
        del ser['_ref_count']
        ser['_operation'] = self.operation.serialize()
        return ser

    def load(self, serialized, **kwargs):
        self._id = serialized['_id']
        self.cmd_text = serialized['_cmd_text']

        operation = serialized['_operation']
        if isinstance(self.operation, MessageOperation):
            at = self.get_param_and_increase(kwargs['places'], operation['at'])
            item = self.get_param_and_increase(kwargs['objects'], operation['item'])
            self.operation.message = operation['message']
            self.operation.at = at
            self.operation.item = item

        if isinstance(self.operation, Requirements):
            for obj in operation['is_carried']:
                obj = self.get_param_and_increase(kwargs['objects'], obj)
                self.operation.is_carried.append(obj)
            for obj in operation['is_present']:
                obj = self.get_param_and_increase(kwargs['objects'], obj)
                self.operation.is_present.append(obj)

        if isinstance(self.operation, FlagOperation):
            at = self.get_param_and_increase(kwargs['places'], operation['at'])
            flag = self.get_param_and_increase(kwargs['flags'], operation['flag'])
            self.operation.success = operation['success']
            self.operation.fail = operation['fail']
            self.operation.flag = flag
            self.operation.at = at
            self.operation.value = operation['value']

        if isinstance(self.operation, CDMOperation):
            for cdm_prop in operation['cdm_props']:
                item = self.get_param_and_increase(kwargs['objects'], cdm_prop['item'])
                self.operation.cdm_props.append(CDMProp(cdm_prop['type'], item))

        if isinstance(self.operation, RelocateOperation):
            from_ = self.get_param_and_increase(kwargs['places'], operation['from_'])
            to = self.get_param_and_increase(kwargs['places'], operation['to'])
            self.operation.success = operation['success']
            self.operation.fail = operation['fail']
            self.operation.can_die = operation['can_die']
            self.operation.from_ = from_
            self.operation.to = to
            
    @staticmethod
    def get_param_and_increase(dictionary: Dict[str, 'ItemNode'], key: str):
        if key in dictionary:
            dictionary[key].ref_count += 1
            return dictionary[key]

        return None
        