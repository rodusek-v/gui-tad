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


class CommonModel(object):
    def __init__(self, model) -> None:
        super().__init__()
        self._model = model
        if self._model.contains:
            self._objects = [Object(o) for o in self._model.contains.objects]
        else:
            self._objects = []

    def name(self):
        return self._model.name 

    def describe(self):
        return self._model.description.description.strip()

    def pretty_name(self):
        return self._model.description.name.strip()

    def get_objects(self):
        return self._objects

    def remove_object(self, object):
        if self._model.contains:
            self._model.contains.objects.remove(object.get_model())
            self._objects.remove(object)
    
    def add_object(self, object):
        if self._model.contains:
            self._model.contains.objects.append(object.get_model())
            self._objects.append(object)

    def get_model(self):
        return self._model


class Place(CommonModel):

    def __init__(self, model) -> None:
        super().__init__(model)
        if self._model.blockade:
            self._blocks = {}
            for block in self._model.blockade.blocks:
                self._blocks[block.direction] = block
        else:
            self._blocks = {}

    def get_blocks(self):
        return self._blocks


class Object(CommonModel):

    def __init__(self, model) -> None:
        super().__init__(model)

    def is_pickable(self):
        return self._model.pickable


class Player(object):

    def __init__(self, model) -> None:
        super().__init__()
        self._model = model
        self._position = Place(self._model.position)
        self._inventory = self.objects = [Object(i) for i in self._model.items]

    def get_position(self):
        return self._position

    def set_position(self, position):
        self._position = Place(position)

    def get_inventory(self):
        return self._inventory

    def remove_from_inventory(self, object):
        self._model.items.remove(object.get_model())
        self._inventory.remove(object)
    
    def add_to_inventory(self, object):
        self._model.items.append(object.get_model())
        self._inventory.append(object)


class World(object):
    
    def __init__(self, model) -> None:
        super().__init__()
        self._places = [Place(p) for p in model.places]
        self._flags = model.flags.flags
        self._player = Player(model.player)
        self._response = ""
        self._reset_console = False
        self.__load_connections(model.connections.connections)
    
    def __load_connections(self, connections):
        self._connections = {}
        for conn in connections:
            from_conn = {
                "direction": conn.direction,
                "to": conn.to_
            }

            to_conn = {
                "direction": opposite_directions[conn.direction],
                "to": conn.from_
            }
            if conn.from_.name not in self._connections:
                self._connections[conn.from_.name] = [from_conn]
            else:
                self._connections[conn.from_.name].append(from_conn)

            if conn.to_.name not in self._connections:
                self._connections[conn.to_.name] = [to_conn]
            else:
                self._connections[conn.to_.name].append(to_conn)

    def __check_block(self, blocks, direction):
        return direction not in blocks or blocks[direction].flag.activated


    def get_places(self):
        return self._places

    def get_connections(self):
        return self._connections

    def get_player(self):
        return self._player

    def get_response(self):
        ret_val = self._response
        self._response = ""
        return ret_val

    def is_console_resetable(self):
        ret_val = self._reset_console
        self._reset_console = False
        return ret_val

    def available_directions(self):
        place = self._player.get_position()
        dirs = []
        blocks = place.get_blocks()
        if place.name() in self._connections:
            for conn in self._connections[place.name()]:
                if self.__check_block(blocks, conn["direction"]):
                    dirs.append(directions[conn["direction"]])

        return dirs

    def check_flags(self):
        pass

    def __move(self, predicate):
        exist = False
        place = self._player.get_position()
        blocks = place.get_blocks()
        if place.name() in self._connections:
            for conn in self._connections[place.name()]:
                if conn["direction"] == predicate and self.__check_block(blocks, conn["direction"]):
                    self._player.set_position(conn["to"])
                    exist = True
                    self._reset_console = True
                    break
        if not exist:
            self._response = "You can't go in that direction."

    def __take(self, predicate, object_name):
        found = False
        place = self._player.get_position()

        if object_name == "ALL":
            if len(place.get_objects()) == 0:
                self._response = f"You can't {predicate.lower()} anything."
                return

        for object in place.get_objects():
            if object.name().upper() == object_name or object_name == "ALL":
                if object.is_pickable():
                    place.remove_object(object)
                    self._player.add_to_inventory(object)
                    self._reset_console = True
                    if object_name != "ALL":
                        found = True
                        break 
                else:
                    self._response = f"You can't take {object.name()}"
                    return
        
        if not found and object_name != "ALL":
            self._response = "You can't find it."

    def __drop(self, object_name):
        found = False
        place = self._player.get_position()

        if object_name == "ALL":
            if len(self._player.get_inventory()) == 0:
                self._response = "You can't drop anything."
                return

        for object in self._player.get_inventory():
            if object.name().upper() == object_name or object_name == "ALL":
                self._player.remove_from_inventory(object)
                place.add_object(object)
                self._reset_console = True
                if object_name != "ALL":
                    found = True
                    break
        
        if not found and object_name != "ALL":
            self._response = "You dont't have it."

    def execute_command(self, command):
        command = check_command(command)
        predicate = command[PREDICATE]

        if predicate in directions or predicate == "GO":
            direction = predicate
            if predicate == "GO":
                direction = command[OBJECT]
                if direction not in directions:
                    self._response = f"I don't know how to {predicate.lower()}"
                    return
            
            self.__move(direction)
                
        elif predicate in ["GET", "TAKE"]:
            object_name = command[OBJECT]
            self.__take(predicate, object_name)
        elif predicate == "DROP":
            object_name = command[OBJECT]
            self.__drop(object_name)
        elif predicate == "I":
            self._response = "INVENTORY"
        elif predicate == "LOOK":
            self._reset_console = True
        else:
            self._response = f"I don't know how to {predicate.lower()}"
