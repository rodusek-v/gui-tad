directions = {
    "N" : "(N) North",
    "W" : "(W) West",
    "S" : "(S) South",
    "E" : "(E) East"
}

full_names = {
    "NORTH": "N",
    "WEST": "W",
    "SOUTH": "S",
    "EAST": "E"
}

opposite_directions = {
    "N" : "S",
    "W" : "E",
    "S" : "N",
    "E" : "W"
}

PREDICATE = 0
OBJECT = 1


def check_command(string):
    split = string.upper().split()
    if len(split) > 2:
        raise Exception("Command must contain maximum two words")

    return split


class ObjectListInterface:

    def add_object(self, object):
        pass

    def remove_object(self, object):
        pass


class CommonModel(ObjectListInterface):
    def __init__(
        self, 
        parent=None,
        name=None, 
        description=None, 
        contains=None
    ) -> None:
        super().__init__()
        self.name = name
        self.description = description
        self.contains = contains

    def get_name(self):
        return self.name.strip().upper()

    def describe(self):
        return self.description.description.strip()

    def pretty_name(self):
        return self.description.name.strip()

    def get_objects(self):
        return self.contains.objects

    def remove_object(self, object):
        try:
            self.contains.objects.remove(object)
            object.set_container()
        except ValueError:
            pass
    
    def add_object(self, object):
        self.contains.objects.append(object)
        object.set_container(self)


class Place(CommonModel):

    def __init__(
        self,
        parent=None, 
        name=None, 
        description=None, 
        contains=None, 
        blockade=None,
        turns_in=None
    ) -> None:
        super().__init__(parent=parent, name=name, description=description, contains=contains)
        self.turns_in = turns_in
        self.blockade = blockade
        if self.blockade:
            self.blocks = {}
            for block in self.blockade.blocks:
                self.blocks[block.direction] = block
        else:
            self.blocks = {}

    def get_blocks(self):
        return self.blocks

    def check_blockade(self):
        for _, block in self.blocks.items():
            if block.turns is not None and block.turns.value <= self.turns_in \
                and not block.flag.activated:
                return block.flag.action_false.message
        return ""

    def increase_turns(self):
        self.turns_in += 1

    def reset_turns(self):
        self.turns_in = 0


class Object(CommonModel):

    def __init__(
        self,
        parent=None, 
        name=None, 
        description=None, 
        contains=None,
        pickable=None,
        container=None
    ) -> None:
        super().__init__(parent=parent, name=name, description=description, contains=contains)
        self.pickable = pickable
        self.container = container

    def is_pickable(self):
        return self.pickable

    def get_container(self):
        return self.container

    def set_container(self, container=None):
        self.container = container


class Player(ObjectListInterface):

    def __init__(
        self,
        parent=None,
        name=None,
        position=None,
        items=None
    ) -> None:
        super().__init__()
        self.name = name
        self.position = position
        self.items = items

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position.reset_turns()
        self.position = position

    def get_inventory(self):
        return self.items

    def remove_object(self, object):
        try:
            self.items.remove(object)
            object.set_container()
        except ValueError:
            pass
    
    def add_object(self, object):
        self.items.append(object)
        object.set_container(self)
