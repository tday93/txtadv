import dill as pickle
import os
import logging
import atexit
from ui import Commander
from game.helpers import datahandlers
from game.helpers.input_parse import parse_player_input as parse_input

logger = logging.getLogger("txtadv")


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

    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.pc = None
        # load game
        self.world = datahandlers.build_world(self)
        self.actions = datahandlers.build_actions(self)
        # rooms, actors, and items are covered by build_rooms()
        self.rooms = datahandlers.build_rooms(self)
        self.world.rooms = self.rooms
        datahandlers.build_exits(self)

    def game_tick(self, player_input):

        # world acts
        # run npc shit
        for room in self.rooms:
            for actor in self.rooms[room].actors:
                actor.do_action()
        # player acts
        # REWRITE HAPPENING HERE
        try:
            action, target, extra = parse_input(self, self.pc,
                                                player_input)
            self.pc.use_action(action, target, **extra)
        except Exception as e:
            raise e

    def input_text(self, player_input):
        self.game_tick(player_input)

    def output_text(self, text):
        self.ui.output(text)

    def set_ui(self, ui):
        self.ui = ui


def save_game(save_file, game_obj):
    with open(save_file, "wb") as fo:
        pickle.dump(game_obj, fo)


def load_game(save_file):
    with open(save_file, "rb") as fn:
        return pickle.load(fn)


def main(options):
    save_file = os.path.join(options.save_dir, options.save_name)
    # load saved game if save exists, otherwise start new game

    if os.path.isfile(save_file):
        game = load_game(save_file)
    else:
        game = Game(options.base_dir)
    atexit.register(save_game, save_file, game)
    c = Commander('ADVENTURE THE GAME', game)
    # start main loop
    game.set_ui(c)
    c.loop()


if __name__ == "__main__":
    main()
