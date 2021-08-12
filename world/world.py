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

    def get_object_by_name(self, name):
        return next(o for o in self._objects if o.name() == name)

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
        self._object_defs = [Object(o) for o in model.objects.objects]
        self._flags = model.flags.flags
        self._player = Player(model.player)
        self._response = ""
        self._reset_console = False
        self.__load_connections(model.connections.connections)
        self.__load_commands(model.commands.commands)
    
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
            from_ = conn.from_.name.strip().upper()
            to_ = conn.to_.name.strip().upper()
            self._connections.setdefault(from_, []).append(from_conn)
            self._connections.setdefault(to_, []).append(to_conn)

    def __load_commands(self, commands):
        self._commands = {}
        for command in commands:
            temp = {}
            for operation in command.operations:
                if operation.object:
                    temp[operation.object.strip().upper()] = operation
                else:
                    temp["None"] = operation

            for predicate in command.names:
                key = predicate.strip().upper()
                self._commands[key] = temp

    def __check_block(self, blocks, direction):
        return direction not in blocks or blocks[direction].flag.activated


    def get_places(self):
        return self._places

    def get_connections(self):
        return self._connections

    def get_commands(self):
        return self._get_commands

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

    def check_flags(self, flag):
        ind = True
        if flag.dependencies:
            for dependency in flag.dependencies:
                ind = ind and dependency.activated
        
        return ind
                
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

            to_remove = []
            for object in place.get_objects():
                if object.is_pickable():
                    to_remove.append(object)
            
            for o in to_remove:
                place.remove_object(o)
                self._player.add_to_inventory(o)
            self._reset_console = True
            return

        for object in place.get_objects():
            if object.name() == object_name:
                if object.is_pickable():
                    place.remove_object(object)
                    self._player.add_to_inventory(object)
                    self._reset_console = True
                    found = True
                    break 
                else:
                    self._response = f"You can't take {object.name()}"
                    return
        
        if not found:
            self._response = "You can't find it."

    def __drop(self, object_name):
        found = False
        place = self._player.get_position()

        if object_name == "ALL":
            if len(self._player.get_inventory()) == 0:
                self._response = "You can't drop anything."
            
            to_remove = []
            for object in self._player.get_inventory():
                to_remove.append(object)
            
            for o in to_remove:
                self._player.remove_from_inventory(o)
                place.add_object(o)

            self._reset_console = True
            return

        for object in self._player.get_inventory():
            if object.name() == object_name:
                self._player.remove_from_inventory(object)
                place.add_object(object)
                self._reset_console = True
                found = True
                break
        
        if not found:
            self._response = "You dont't have it."

    def __execute_crud(self, crud_prop, place, object):
        crud_item = Object(crud_prop.item)
        if crud_prop.type == 'create':
            place.add_object(crud_item)
        elif crud_prop.type == 'delete':
            place.remove_object(crud_item)
        elif crud_prop.type == 'move':
            object.remove_object(crud_item)
            place.add_object(crud_item)

    def __eval_requirements(self, operation, place):
        ind_place = True
        ind_inv = True
        for req in operation.require_prop:
            if req.__class__.__name__ == "RequirePlaceProp":
                ind_place = ind_place and all(Object(item) in place.get_objects() for item in req.require)
            elif req.__class__.__name__ == "RequireInventoryProp":
                ind_inv = ind_inv and all(Object(item) in self._player.get_inventory() for item in req.require)
        return ind_place, ind_inv

    def __eval_location(self, operation, place):
        ind = True
        if operation.located_prop:
            req_place = Place(operation.located_prop.located) 
            ind = ind and req_place == place 

        return ind

    def __specific_command(self, predicate, object_name):
        place = self._player.get_position()
        commands = self._commands

        if predicate in commands:
            if object_name in commands[predicate]:
                operation = commands[predicate][object_name]
                if operation.type.__class__.__name__ == "MessageOperation":
                    self._response = operation.type.message
                elif operation.type.__class__.__name__ == "CRUDOperation":
                    operation = operation.type
                    req_place, req_inventory = self.__eval_requirements(operation, place)
                    loc_ind = self.__eval_location(operation, place)
                    if loc_ind and req_place:
                        if req_inventory:
                            if operation.flag_prop:
                                flag = operation.flag_prop.flag
                                value = operation.flag_prop.value
                                if flag.activated == value:
                                    if self.check_flags(flag):
                                        self.__execute_crud(operation.crud_prop, place, place.get_object_by_name(object_name))
                                        flag.activated = not value
                                        self._response = operation.success
                                    else:
                                        self._response = operation.fail
                                else:
                                    self._response = flag.message
                            else:
                                self.__execute_crud(operation.crud_prop, place, place.get_object_by_name(object_name))
                                self._response = operation.success
                        else:
                            self._response = operation.fail
                    else:
                        self._response = f"I don't see any {object_name}"
                        
                elif operation.type.__class__.__name__ == "FlagOperation":
                    operation = operation.type
                    flag = operation.flag_prop.flag
                    value = operation.flag_prop.value
                    req_place, req_inventory = self.__eval_requirements(operation, place)
                    loc_ind = self.__eval_location(operation, place)
                    if loc_ind and req_place:
                        if flag.activated == value:
                            if req_inventory and self.check_flags(flag):
                                flag.activated = not value
                                self._response = operation.success
                            else:
                                self._response = operation.fail
                        else:
                            self._response = flag.message
                    else:
                        self._response = f"I don't see any {object_name}"
            else:
                self._response = "I can't do that."
        else:
            self._response = f"I don't know how to {predicate.lower()}"

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
            object_name = command[OBJECT] if len(command) == 2 else "None"
            self.__specific_command(predicate, object_name)
                
