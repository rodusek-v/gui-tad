from typing import List
from jinja2 import Template


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

    def __init__(self, flag: 'Flag', direction: str, turns: int = None) -> None:
        self.flag = flag
        self.direction = direction
        self.turns = turns


class Action:

    def __init__(self, message: str = None, dependecines: List['Dependency'] = None) -> None:
        self.message = message
        if dependecines is None:
            dependecines = []
        self.dependecines = dependecines

    def get_dependecines(self) -> List['Dependency']:
        return self.dependecines

    def add_dependency(self, dependency: 'Dependency') -> None:
        self.dependecines.append(dependency)

    def remove_dependency(self, dependency: 'Dependency') -> None:
        self.dependecines.remove(dependency)


class Dependency:

    def __init__(self, flag: 'Flag', value: bool) -> None:
        self.flag = flag
        self.value = value


from model.flag import Flag