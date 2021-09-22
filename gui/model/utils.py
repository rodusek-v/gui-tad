import jinja2
from enum import Enum
from typing import List


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
            templateLoader = jinja2.FileSystemLoader(searchpath="./")
            templateEnv = jinja2.Environment(loader=templateLoader)
            t = templateEnv.get_template(template_path)
            ret_val = t.render(model=self)
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

    def __init__(self, message: str = "", dependencies: List['Dependency'] = None) -> None:
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

    def __str__(self) -> str:
        deps = ""
        if len(self.dependencies) != 0:
            deps = "dependencies: ["
            deps += ", ".join([f"{dep.flag.name} == {str(dep.value).lower()}" for dep in self.dependencies])
            deps += "]"
        return f"""
            message: "{self.message}"
            {deps}
        """


class Dependency:

    def __init__(self, flag: 'Flag', value: bool) -> None:
        self.flag = flag
        self.value = value

    def serialize(self):
        ser = dict(self.__dict__)
        ser['flag'] = self.flag.name

        return ser


from model.flag import Flag