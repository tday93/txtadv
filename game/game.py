import pickle
import os
import sys
import logging
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

    def game_loop(self):
        while True:
            # world acts
            # player acts
            player_input = self.input_text()
            os.system("clear")
            # REWRITE HAPPENING HERE
            try:
                action, target, extra = parse_input(self, self.pc,
                                                    player_input)
                self.pc.use_action(action, target, **extra)
            except Exception as e:
                raise e
            # npcs act

    def input_text(self):
        # this should change
        text = input("\nWhat do?\n")
        return text

    def output_text(self, text):
        # this should also change
        print(text)


def save_game(save_file, game_obj):
    with open(save_file, "wb") as fo:
        pickle.dump(game_obj, fo)


def load_game(save_file):
    with open(save_file, "rb") as fn:
        return pickle.load(fn)


def main(options):
    save_file = os.path.join(options.save_dir, options.save_name)
    # load saved game if save exists, otherwise start new game
    try:
        if os.path.isfile(save_file):
            game = load_game(save_file)
        else:
            game = Game(options.base_dir)
        game.game_loop()
    except KeyboardInterrupt:
        save_game(save_file, game)
        sys.exit(0)


if __name__ == "__main__":
    main()
