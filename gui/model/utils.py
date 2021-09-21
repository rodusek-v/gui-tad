from enum import Enum
from typing import List
from jinja2 import Template


class Sides(Enum):
    N = "N"
    S = "S"
    W = "W"
    E = "E"


class TextModel:
    
    def __init__(self) -> None:
        pass

    def text_model(self, template_path: str) -> str:
        ret_val = ""
        try:
            t = Template(template_path)
            ret_val = t.render(self=self)
        except Exception as ex:
            print(ex)

        return ret_val


class Description:

    def __init__(self, name:str = "", description: str = "") -> None:
        self.name = name
        self.description = description


class Block:

    def __init__(self, flag: 'Flag', direction: Sides, turns: int = -1) -> None:
        self.flag = flag
        self.direction = direction
        self.turns = turns

    def serialize(self):
        ser = dict(self.__dict__)
        ser['flag'] = self.flag.name
        return ser


class Action:

    def __init__(self, message: str = None, dependencies: List['Dependency'] = None) -> None:
        self.message = message
        if dependencies is None:
            dependencies = []
        self.dependencies = dependencies

    def get_dependencies(self) -> List['Dependency']:
        return self.dependencies

    def add_dependency(self, dependency: 'Dependency') -> None:
        self.dependencies.append(dependency)

    def remove_dependency(self, dependency: 'Dependency') -> None:
        self.dependencies.remove(dependency)

    def serialize(self):
        ser = dict(self.__dict__)
        ser['dependencies'] = [dep.serialize() for dep in self.dependencies]
        return ser


class Dependency:

    def __init__(self, flag: 'Flag', value: bool) -> None:
        self.flag = flag
        self.value = value

    def serialize(self):
        ser = dict(self.__dict__)
        ser['flag'] = self.flag.name

        return ser


from model.flag import Flag