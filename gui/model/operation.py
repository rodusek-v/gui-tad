from enum import Enum
from typing import List


class CDMType(Enum):
    CREATE = "create"
    DELETE = "delete"
    MOVE = "move"


class OperationType(Enum):
    MESSAGE_OPERATION = 0
    FLAG_OPERATION = 1
    CDM_OPERATION = 2
    RELOCATION_OPERATION = 3


class Operation(object):

    def __init__(self) -> None:
        super().__init__()

    @property
    def props(self):
        pass

    @property
    def type(self) -> OperationType:
        pass

    def decrease_refferees(self):
        pass
    

class MessageOperation(Operation):

    def __init__(self) -> None:
        super().__init__()
        self.message: str = ""
        self.item: 'Object' = None
        self.at: 'Place' = None

    @property
    def type(self) -> OperationType:
        return OperationType.MESSAGE_OPERATION

    @property
    def props(self):
        attrs = dict(self.__dict__)
        if self.item is not None:
            attrs["item"] = self.item.name
        else:
            del attrs["item"]
        if self.at is not None:
            attrs["at"] = self.at.name
        else:
            del attrs["at"]
        return attrs

    def decrease_refferees(self):
        if self.at:
            self.at.ref_count -= 1
        if self.item:
            self.item.ref_count -= 1


class Requirements(Operation):

    def __init__(self) -> None:
        super().__init__()
        self.is_present: List['Object'] = []
        self.is_carried: List['Object'] = []

    @property
    def props(self):
        attrs = dict(self.__dict__)
        if len(self.is_present) == 0:
            del attrs["is_present"]
        else:
            attrs["is_present"] = f"[{','.join([item.name for item in self.is_present])}]"

        if len(self.is_carried) == 0:
            del attrs["is_carried"]
        else:
            attrs["is_carried"] = f"[{','.join([item.name for item in self.is_carried])}]"
        return attrs

    def decrease_refferees(self):
        for item in self.is_carried:
            item.ref_count -= 1
        for item in self.is_present:
            item.ref_count -= 1


class FlagOperation(Requirements):

    def __init__(self) -> None:
        super().__init__()
        self.flag: 'Flag' = None
        self.value: bool = True
        self.success: str = None
        self.fail: str = None
        self.at: 'Place' = None

    @property
    def type(self) -> OperationType:
        return OperationType.FLAG_OPERATION

    @property
    def props(self):
        attrs = super().props
        del attrs["value"]
        if self.at is not None:
            attrs["at"] = self.at.name
        else:
            del attrs["at"]
        if self.flag is not None:
            attrs["flag"] = f"{self.flag.name} == {str(self.value).lower()}"
        else:
            del attrs["flag"]
        return attrs

    def decrease_refferees(self):
        super().decrease_refferees()
        if self.flag:
            self.flag.ref_count -= 1
        if self.at:
            self.at.ref_count -= 1

class CDMOperation(FlagOperation):

    def __init__(self) -> None:
        super().__init__()
        self.cdm_props: List['CDMProp'] = []

    @property
    def type(self) -> OperationType:
        return OperationType.CDM_OPERATION

    @property
    def props(self):
        attrs = super().props
        del attrs['cdm_props']
        for cdm in self.cdm_props:
            attrs[cdm.type.value] = cdm.item.name
        return attrs

    def decrease_refferees(self):
        super().decrease_refferees()
        for cdm in self.cdm_props:
            cdm.item.ref_count -= 1


class RelocateOperation(Requirements):

    def __init__(self) -> None:
        super().__init__()
        self.from_: 'Place' = None
        self.to: 'Place' = None
        self.success: str = None
        self.fail: str = None
        self.can_die: bool = False

    @property
    def type(self) -> OperationType:
        return OperationType.RELOCATION_OPERATION

    @property
    def props(self):
        attrs = super().props
        del attrs["from_"]
        attrs["from"] = self.from_.name
        attrs["to"] = self.to.name
        attrs["can_die"] = str(self.can_die).lower()
        
        return attrs

    def decrease_refferees(self):
        super().decrease_refferees()
        if self.to:
            self.to.ref_count -= 1
        if self.from_:
            self.from_.ref_count -= 1

class CDMProp:

    def __init__(self, type: 'CDMType' = None, item: 'Object' = None):
        self.type: 'CDMType' = type
        self.item: 'Object' = item


from model.flag import Flag
from model.object import Object
from model.place import Place
