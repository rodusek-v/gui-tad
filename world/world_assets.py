directions = {
    "N" : "(N) North",
    "W" : "(W) West",
    "S" : "(S) South",
    "E" : "(E) East"
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
    def __init__(self, model) -> None:
        super().__init__()
        self._model = model
        if self._model.contains:
            self._objects = [Object(o) for o in self._model.contains.objects]
        else:
            self._objects = []

    def __eq__(self, o) -> bool:
        if isinstance(o, CommonModel):
            return o.name() == self.name()

        return False

    def name(self):
        return self._model.name.strip().upper()

    def describe(self):
        return self._model.description.description.strip()

    def pretty_name(self):
        return self._model.description.name.strip()

    def get_objects(self):
        return self._objects

    def remove_object(self, object):
        if self._model.contains:
            self._model.contains.objects.remove(object.get_model())
            object.set_container()
            self._objects.remove(object)
    
    def add_object(self, object):
        if self._model.contains:
            self._model.contains.objects.append(object.get_model())
            object.set_container(self._model)
            self._objects.append(object)

    def get_model(self):
        return self._model


class Place(CommonModel):

    def __init__(self, model) -> None:
        super().__init__(model)
        self._turns_in = 0
        if self._model.blockade:
            self._blocks = {}
            for block in self._model.blockade.blocks:
                self._blocks[block.direction] = block
        else:
            self._blocks = {}

    def get_blocks(self):
        return self._blocks

    def check_blockade(self):
        for _, block in self._blocks.items():
            if block.turns is not None and block.turns.value <= self._turns_in \
                and not block.flag.activated:
                return True
        return False

    def increase_turns(self):
        self._turns_in += 1

    def reset_turns(self):
        self._turns_in = 0


class Object(CommonModel):

    def __init__(self, model) -> None:
        super().__init__(model)

    def is_pickable(self):
        return self._model.pickable

    def get_container(self):
        return self._model.container

    def set_container(self, container=None):
        self._model.container = container


class Player(ObjectListInterface):

    def __init__(self, model) -> None:
        super().__init__()
        self._model = model
        self._position = Place(self._model.position)
        self._inventory = [Object(i) for i in self._model.items]

    def get_position(self):
        return self._position

    def set_position(self, position):
        self._position.reset_turns()
        self._position = position

    def get_inventory(self):
        return self._inventory

    def remove_object(self, object):
        self._model.items.remove(object.get_model())
        object.set_container()
        self._inventory.remove(object)
    
    def add_object(self, object):
        self._model.items.append(object.get_model())
        object.set_container(self._model)
        self._inventory.append(object)
