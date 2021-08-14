from os.path import join, dirname
from textx import metamodel_from_file
from world.world import World
from utils.utils import clear, getch

class GameCmd(object):
    
    def __init__(self, model) -> None:
        super().__init__()
        self._world = World(model)

    def _print_place_description(self):
        print(self._world.get_player().get_position().describe())

    def _print_inventory(self):
        print("You're carrying:")
        if len(self._world.get_player().get_inventory()) == 0:
            print("\tNothing")
        else:
            for item in self._world.get_player().get_inventory():
                print("\t" + item.pretty_name())

    def _print_place_objects(self):
        place_objects = self._world.get_player().get_position().get_objects()
        
        if len(place_objects) != 0:
            print("You can see", end=" ")
            for index, object in enumerate(place_objects):
                if index == len(place_objects) - 1:
                    print(f"{object.pretty_name()}.")
                elif index == len(place_objects) - 2:
                    print(f"{object.pretty_name()} and", end=" ")
                else:
                    print(f"{object.pretty_name()},", end=" ")

    def _print_directions(self):
        print("Directions:", end=" ")
        for direction in self._world.available_directions():
            print(f"{direction}", end=" ")
        print()

    def _print_menu(self):
        self._print_place_description()
        self._print_place_objects()
        self._print_directions()

    def play(self):
        clear()
        self._print_menu()
        while True:
            try:
                if self._world.wait_enter():
                    print("\t\t\t\tPress enter to continue...")
                    while getch() != '\r':
                        pass

                    clear()
                    self._print_menu()
                else:
                    command = input(">")
                    self._world.execute_command(command)
                    response = self._world.get_response()
                    if response != "":
                        if response == "INVENTORY":
                            self._print_inventory()
                        else:
                            print(response)

                    if self._world.is_finished():
                        break

                    if self._world.is_console_resetable():
                        clear()
                        self._print_menu()
            except Exception as ex:
                print(ex)


if __name__ == '__main__':
    this_folder = dirname(__file__)
    meta_model = metamodel_from_file(join(this_folder, 'textx/world.tx'))
    model = meta_model.model_from_file(join(this_folder, 'textx/test.wld'))
    game = GameCmd(model)
    game.play()
