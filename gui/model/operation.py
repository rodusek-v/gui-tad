from enum import Enum
from typing import List


class CMDType(Enum):
    CREATE = "create"
    DELETE = "delete"
    MOVE = "move"


class Operation(object):

    def __init__(self) -> None:
        super().__init__()

    @property
    def props(self):
        pass
    

class MessageOperation(Operation):

    def __init__(self) -> None:
        super().__init__()
        self.message: str = ""
        self.item: 'Object' = None
        self.at: 'Place' = None

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


class FlagOperation(Requirements):

    def __init__(self) -> None:
        super().__init__()
        self.flag: 'Flag' = None
        self.value: bool = None
        self.success: str = None
        self.fail: str = None
        self.at: 'Place' = None

    @property
    def props(self):
        attrs = super().props
        if self.at is not None:
            attrs["at"] = self.at.name
        else:
            del attrs["at"]
        if self.flag is not None:
            attrs["flag"] = f"{self.flag.name} == {str(self.value).lower()}"
        else:
            del attrs["flag"]
        return attrs

class CDMOperation(FlagOperation):

    def __init__(self) -> None:
        super().__init__()
        self.cdm_props: List['CDMProp'] = None

    @property
    def props(self):
        attrs = super().props
        del attrs['cdm_props']
        for cdm in self.cdm_props:
            attrs[cdm.type.value] = cdm.item.name
        return attrs


class RelocateOperation(Requirements):

    def __init__(self) -> None:
        super().__init__()
        self.from_: 'Place' = None
        self.to: 'Place' = None
        self.success: str = None
        self.fail: str = None
        self.can_die: bool = None

    @property
    def props(self):
        attrs = super().props
        del attrs["from_"]
        attrs["from"] = self.from_.name
        attrs["to"] = self.to.name
        attrs["can_die"] = str(self.can_die).lower()
        
        return attrs

class CDMProp:

    def __init__(self):
        self.type: 'CMDType' = None
        self.item: 'Object' = None


from model.flag import Flag
from model.object import Object
from model.place import Place
