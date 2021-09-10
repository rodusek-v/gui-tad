from jinja2 import Template


class TextModel:
    
    def __init__(self) -> None:
        pass

    def text_model(self, template_path):
        ret_val = ""
        try:
            t = Template(template_path)
            ret_val = t.render(self=self)
        except Exception as ex:
            print(ex)

        return ret_val


class Description:

    def __init__(self, name="", description="") -> None:
        self.name = name
        self.description = description


class Block:

    def __init__(self, flag, direction, turns=None) -> None:
        self.flag = flag
        self.direction = direction
        self.turns = turns


class Operation(object):

    def __init__(self) -> None:
        super().__init__()

    @property
    def props(self):
        pass
    

class MessageOperation(Operation):

    def __init__(self) -> None:
        super().__init__()
        self.message = None
        self.item = None
        self.at = None

    @property
    def props(self):
        attrs = dict(self.__dict__)
        attrs["item"] = attrs["item"].name
        attrs["at"] = attrs["at"].name
        return attrs


class Requirements(Operation):

    def __init__(self) -> None:
        super().__init__()
        self.is_present = None
        self.is_carried = None

    @property
    def props(self):
        attrs = dict(self.__dict__)
        if self.is_present is None:
            del attrs["is_present"]
        else:
            attrs["is_present"] = f"[{','.join([item.name for item in self.is_present])}]"

        if self.is_carried is None:
            del attrs["is_carried"]
        else:
            attrs["is_carried"] = f"[{','.join([item.name for item in self.is_carried])}]"
        return attrs


class FlagOperation(Requirements):

    def __init__(self) -> None:
        super().__init__()
        self.flag = None
        self.success = None
        self.fail = None
        self.at = None

    @property
    def props(self):
        attrs = super().props 
        attrs["at"] = attrs["at"].name
        attrs["flag"] = f"{self.flag.flag.name} == {str(self.flag.value).lower()}"
        return attrs

class CDMOperation(FlagOperation):

    def __init__(self) -> None:
        super().__init__()
        self.cdm_props = None

    @property
    def props(self):
        attrs = super().props
        del attrs['cdm_props']
        for cdm in self.cdm_props:
            attrs[cdm.type] = cdm.item.name
        return attrs


class RelocateOperation(Requirements):

    def __init__(self) -> None:
        super().__init__()
        self.from_ = None
        self.to = None
        self.success = None
        self.fail = None
        self.can_die = None

    @property
    def props(self):
        attrs = super().props
        del attrs["from_"]
        attrs["from"] = self.from_.name
        attrs["to"] = self.to.name
        attrs["can_die"] = str(self.can_die).lower()
        
        return attrs