import datahandlers

BASE_DIR = "./data"
ITEM_DIR = BASE_DIR + "/items"
ACTION_DIR = BASE_DIR + "/actions"
ACTOR_DIR = BASE_DIR + "/actors"
ROOM_DIR = BASE_DIR + "/rooms"
EXIT_DIR = BASE_DIR + "/exits"


class Game(object):

    """
        The encompassing object for the rest of the game.
        It manages:
            Loading objects into the game
            Player input/output
            The main loop
            Saving the game on exit

        It is the parent object for the world object and action objects
    """

    def __init__(self):
        self.pc = None
        # load game
        self.world = datahandlers.build_world(self, BASE_DIR)
        self.actions = datahandlers.build_actions(self)
        # rooms, actors, and items are covered by build_rooms()
        self.rooms = datahandlers.build_rooms(self)
        self.world.rooms = self.rooms
        datahandlers.build_exits(self)
        # start main game loop
        # save game

    def game_loop(self):
        while True:
            p_input = self.input_text()
            cmd = p_input.split(" ", 1)[0]
            self.pc.use_action(cmd, p_input)

    def input_text(self):
        # this should change
        text = input("\nWhat do?\n")
        return text

    def output_text(self, text):
        # this should also change
        print(text)


if __name__ == "__main__":
    game = Game()
    game.game_loop()
