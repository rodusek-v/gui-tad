from typing import List
from PyQt6.QtCore import QObject

from model import Command, Place, Object, Flag
from model.operation import CDMOperation, CDMProp, CDMType, FlagOperation,\
     MessageOperation, OperationType, RelocateOperation, Requirements


class CommandController(QObject):

    def __init__(self, model: Command) -> None:
        super().__init__()
        self._model = model

    @property
    def model(self) -> Command:
        return self._model

    @model.setter
    def model(self, value: Command) -> None:
        self._model = value

    def get_cmd_text(self) -> List[str]:
        return self.model.cmd_text

    def set_cmd_text(self, value: List[str]) -> None:
        self.model.cmd_text = value

    def get_type(self) -> OperationType:
        return self.model.operation.type

    def set_message(self, message: str) -> None:
        operation = self.model.operation
        if isinstance(operation, MessageOperation):
            operation.message = message
            
    def get_message(self) -> str:
        operation = self.model.operation
        if isinstance(operation, MessageOperation):
            return operation.message

    def set_item(self, item: 'Object') -> None:
        operation = self.model.operation
        if isinstance(operation, MessageOperation):
            if operation.item is not None:
                operation.item.ref_count -= 1
            operation.item = item
            if operation.item is not None:
                operation.item.ref_count += 1

    def get_item(self) -> 'Object':
        operation = self.model.operation
        if isinstance(operation, MessageOperation):
            return operation.item

    def set_at(self, place: 'Place') -> None:
        operation = self.model.operation
        if isinstance(operation, MessageOperation) or isinstance(operation, FlagOperation):
            if operation.at is not None:
                operation.at.ref_count -= 1
            operation.at = place
            if operation.at is not None:
                operation.at.ref_count += 1

    def get_at(self) -> 'Place':
        operation = self.model.operation
        if isinstance(operation, MessageOperation) or isinstance(operation, FlagOperation):
            return operation.at

    def set_flag(self, flag: 'Flag') -> None:
        operation = self.model.operation
        if isinstance(operation, FlagOperation):
            operation.flag = flag

    def get_flag(self) -> 'Flag':
        operation = self.model.operation
        if isinstance(operation, FlagOperation):
            return operation.flag

    def set_value(self, value: bool) -> None:
        operation = self.model.operation
        if isinstance(operation, FlagOperation):
            operation.value = value

    def get_value(self) -> bool:
        operation = self.model.operation
        if isinstance(operation, FlagOperation):
            return operation.value

    def set_success(self, value: str) -> None:
        operation = self.model.operation
        if isinstance(operation, RelocateOperation) or isinstance(operation, FlagOperation):
            operation.success = value

    def get_success(self) -> str:
        operation = self.model.operation
        if isinstance(operation, RelocateOperation) or isinstance(operation, FlagOperation):
            return operation.success

    def set_fail(self, value: str) -> None:
        operation = self.model.operation
        if isinstance(operation, RelocateOperation) or isinstance(operation, FlagOperation):
            operation.fail = value

    def get_fail(self) -> str:
        operation = self.model.operation
        if isinstance(operation, RelocateOperation) or isinstance(operation, FlagOperation):
            return operation.fail

    def get_carry_requirements(self) -> List['Object']:
        operation = self.model.operation
        if isinstance(operation, Requirements):
            return operation.is_carried

    def add_carry_requirement(self, item: 'Object') -> None:
        operation = self.model.operation
        if isinstance(operation, Requirements):
            item.ref_count += 1
            return operation.is_carried.append(item)

    def remove_carry_requirement(self, item: 'Object') -> None:
        operation = self.model.operation
        if isinstance(operation, Requirements):
            item.ref_count -= 1
            return operation.is_carried.remove(item)

    def get_present_requirements(self) -> List['Object']:
        operation = self.model.operation
        if isinstance(operation, Requirements):
            return operation.is_present

    def add_present_requirement(self, item: 'Object') -> None:
        operation = self.model.operation
        if isinstance(operation, Requirements):
            item.ref_count += 1
            return operation.is_present.append(item)

    def remove_present_requirement(self, item: 'Object') -> None:
        operation = self.model.operation
        if isinstance(operation, Requirements):
            item.ref_count -= 1
            return operation.is_present.remove(item)

    def set_from(self, place: 'Place') -> None:
        operation = self.model.operation
        if isinstance(operation, RelocateOperation):
            if operation.from_ is not None:
                operation.from_.ref_count -= 1
            operation.from_ = place
            if operation.from_ is not None:
                operation.from_.ref_count += 1

    def get_from(self) -> 'Place':
        operation = self.model.operation
        if isinstance(operation, RelocateOperation):
            return operation.from_

    def set_to(self, place: 'Place') -> None:
        operation = self.model.operation
        if isinstance(operation, RelocateOperation):
            if operation.to is not None:
                operation.to.ref_count -= 1
            operation.to = place
            if operation.to is not None:
                operation.to.ref_count += 1

    def get_to(self) -> 'Place':
        operation = self.model.operation
        if isinstance(operation, RelocateOperation):
            return operation.to

    def set_can_die(self, value: bool) -> None:
        operation = self.model.operation
        if isinstance(operation, RelocateOperation):
            operation.can_die = value

    def get_can_die(self) -> bool:
        operation = self.model.operation
        if isinstance(operation, RelocateOperation):
            return operation.can_die

    def get_cdm_props(self) -> List[CDMProp]:
        operation = self.model.operation
        if isinstance(operation, CDMOperation):
            return operation.cdm_props

    def add_cdm_prop(self, type: CDMType, item: 'Object') -> bool:
        operation = self.model.operation
        if isinstance(operation, CDMOperation):
            item.ref_count += 1
            operation.cdm_props.append(CDMProp(type, item))

    def remove_cdm_prop(self, prop: CDMProp) -> bool:
        operation = self.model.operation
        if isinstance(operation, CDMOperation):
            prop.item.ref_count -= 1
            operation.cdm_props.remove(prop)