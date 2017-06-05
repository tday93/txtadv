"""

    give directory containing game, validate all json within that directory

"""
import json
import glob
from os import path
from jsonschema import validate, ValidationError


class JLinter(object):

    def __init__(self, schema_dir, game_dir):
        self.sub_dirs = ["actions", "exits", "items", "actors", "rooms"]
        self.schema_dir = schema_dir
        self.game_dir = game_dir
        print(self.check_game())
        print(self.check_world())
        print(self.check_subdirs())

    def check_subdirs(self):
        for sub_dir in self.sub_dirs:
            print(sub_dir)
            print(self.check_all_in_dir(sub_dir))

    def j_validate(self, schema, test_dict):
        try:
            validate(test_dict, schema)
            return True
        except ValidationError as e:
            raise e
            return False
        except Exception as e:
            raise e

    def load_json(self, path):
        with open(path, "r") as fn:
            test_dict = json.load(fn)
            return test_dict

    def check_game(self):
        # check game.json
        sp = path.join(self.schema_dir, "game.json")
        gp = path.join(self.game_dir, "game.json")
        sd = self.load_json(sp)
        gd = self.load_json(gp)

        return self.j_validate(sd, gd)

    def check_world(self):
        # check world.json
        sp = path.join(self.schema_dir, "world.json")
        wp = path.join(self.game_dir, "world.json")
        sd = self.load_json(sp)
        wd = self.load_json(wp)

        return self.j_validate(sd, wd)

    def check_all_in_dir(self, dir_name):
        sub_dir = path.join(self.game_dir, dir_name)
        sp = path.join(self.schema_dir, dir_name + ".json")
        sd = self.load_json(sp)
        game_paths = glob.glob(sub_dir + "/*.json")
        print(game_paths)
        g_dicts = [self.load_json(g_path) for g_path in game_paths]
        return all(self.j_validate(sd, g_dict) for g_dict in g_dicts)


if __name__ == "__main__":
    jlint = JLinter("/home/tday/projects/games/txtadvmk4/game/helpers/jsonschema",
                    "/home/tday/projects/games/txtadvmk4/data")

