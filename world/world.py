from world.world_assets import *

class World(object):
    
    def __init__(self, model) -> None:
        super().__init__()
        self._places = [Place(p) for p in model.places]
        self._player = Player(model.player)
        self._response = ""
        self._reset_console = False
        self._finish_goal = model.finish
        self._game_over = False
        self._is_finished = False
        self.__load_connections(model.connections.connections)
        self.__load_commands(model.commands.commands)

    def __wrap_container(self, container):
        ret_val = None
        if container.__class__.__name__ in ["Place", "Object"]:
            temp = CommonModel(container)
            for place in self._places:
                if temp == place:
                    ret_val = place
                    break
                else:
                    for obj in place.get_objects():
                        if temp == obj:
                            ret_val = obj
                            break
        elif container.__class__.__name__ == "Player":
            ret_val = self._player
        return ret_val
    
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
            for text in command.text:
                object_name = f" {text.object}" if text.object else ""
                text_ = f"{text.predicate}{object_name}"
                self._commands[text_.strip().upper()] = command.operation

    def __check_block(self, blocks, direction):
        return direction not in blocks or blocks[direction].flag.activated

    def __is_game_finished(self):
        place = self._player.get_position()
        if Place(self._finish_goal.position) == place:
            if self._finish_goal.flag_prop:
                flag_prop = self._finish_goal.flag_prop
                return flag_prop.flag.activated == flag_prop.value
            else:
                return True

    def __check_flags(self, flag):
        ind = True
        if flag.activated:
            for dependency in flag.action_false.dependencies:
                ind = ind and (dependency.flag.activated == dependency.value)
        else:
            for dependency in flag.action_true.dependencies:
                ind = ind and (dependency.flag.activated == dependency.value)
        
        return ind
                
    def __move(self, predicate):
        exist = False
        place = self._player.get_position()
        blocks = place.get_blocks()
        if place.name() in self._connections:
            for conn in self._connections[place.name()]:
                if conn["direction"] == predicate and self.__check_block(blocks, conn["direction"]):
                    self._player.set_position(self.__wrap_container(conn["to"]))
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
                self._player.add_object(o)
            self._reset_console = True
            return

        for object in place.get_objects():
            if object.name() == object_name:
                if object.is_pickable():
                    place.remove_object(object)
                    self._player.add_object(object)
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
                self._player.remove_object(o)
                place.add_object(o)

            self._reset_console = True
            return

        for object in self._player.get_inventory():
            if object.name() == object_name:
                self._player.remove_object(object)
                place.add_object(object)
                self._reset_console = True
                found = True
                break
        
        if not found:
            self._response = "You dont't have it."

    def __execute_crud(self, crud_props):
        for crud_prop in crud_props:
            crud_item = Object(crud_prop.item)
            if crud_prop.type == 'create':
                if crud_item.is_pickable():
                    self._player.add_object(crud_item)
                else:
                    self._player.get_position().add_object(crud_item)
            elif crud_prop.type == 'delete':
                self.__wrap_container(crud_item.get_container()).remove_object(crud_item)
            elif crud_prop.type == 'move':
                self.__wrap_container(crud_item.get_container()).remove_object(crud_item)
                self._player.get_position().add_object(crud_item)

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

    def __execute_crud_operation(self, operation, place, object_name):
        req_place, req_inventory = self.__eval_requirements(operation, place)
        loc_ind = self.__eval_location(operation, place)
        if loc_ind and req_place:
            if req_inventory:
                if operation.flag_prop:
                    flag = operation.flag_prop.flag
                    value = operation.flag_prop.value
                    if flag.activated == value:
                        if self.__check_flags(flag):
                            self.__execute_crud(operation.crud_props)
                            flag.activated = not value
                            self._response = operation.success
                        else:
                            self._response = operation.fail
                    else:
                        if flag.activated:
                            self._response = flag.action_true.message
                        else:
                            self._response = flag.action_false.message
                else:
                    self.__execute_crud(operation.crud_props)
                    self._response = operation.success
            else:
                self._response = operation.fail
        else:
            self._response = f"I don't see any {object_name}" 

    def __execute_flag_operation(self, operation, place, object_name):
        flag = operation.flag_prop.flag
        value = operation.flag_prop.value
        req_place, req_inventory = self.__eval_requirements(operation, place)
        loc_ind = self.__eval_location(operation, place)
        if loc_ind and req_place:
            if flag.activated == value:
                if req_inventory and self.__check_flags(flag):
                    flag.activated = not value
                    self._response = operation.success
                else:
                    self._response = operation.fail
            else:
                if flag.activated:
                    self._response = flag.action_true.message
                else:
                    self._response = flag.action_false.message
        else:
            self._response = f"I don't see any {object_name}"

    def __specific_command(self, predicate, object_name):
        place = self._player.get_position()
        commands = self._commands
        temp = f" {object_name}" if object_name else ""
        command_text = f"{predicate}{temp}"

        if command_text in commands:
            operation = commands[command_text]
            if operation.__class__.__name__ == "MessageOperation":
                self._response = operation.message
            elif operation.__class__.__name__ == "CRUDOperation":
                self.__execute_crud_operation(operation, place, object_name)
            elif operation.__class__.__name__ == "FlagOperation":
                self.__execute_flag_operation(operation, place, object_name)
        else:
            self._response = f"I don't know how to {predicate.lower()}"
    
    def __check_life(self):
        place = self._player.get_position()
        if not place.check_blockade():
            place.increase_turns()
        else:
            self._game_over = True

    
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

    def execute_command(self, command):
        if self._is_finished:
            return

        command = check_command(command)
        if len(command) == 0:
            self._reset_console = True
            return 

        predicate = command[PREDICATE]
    
        try:
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
            elif predicate in ["I", "INVENTORY"]:
                self._response = "INVENTORY"
            elif predicate == "LOOK":
                self._reset_console = True
            else:
                object_name = command[OBJECT] if len(command) == 2 else None
                self.__specific_command(predicate, object_name)
                if self._response == "":
                    self._reset_console = True

            self.__check_life()
        except Exception as ex:
            print(ex)
            self._response = "Oops, can't do that."

        if self.__is_game_finished():
            self._is_finished = True
            self._response = "Congratulations you have successfully finished the game"

        if self._game_over:
            self._is_finished = True
            self._response = "GAME OVER"
        
    def is_finished(self):
        return self._is_finished
