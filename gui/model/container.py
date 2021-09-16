
from typing import List

class Container(object):

    @property
    def name(self) -> str:
        pass

    def add_object(self, object: 'Object') -> None:
        pass

    def get_objects(self) -> List['Object']:
        pass

    def remove_object(self, object: 'Object') -> None:
        pass


from model.object import Object