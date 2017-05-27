import os
import datahelpers
import actions
import actor
from world import World
from room import Room
from item import Item
from exit import Exit

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
        self.world = self.build_world(BASE_DIR)
        self.actions = self.build_actions()
        # rooms, actors, and items are covered by build_rooms()
        self.rooms = self.build_rooms()
        self.world.rooms = self.rooms
        self.build_exits()
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

    def build_actions(self):
        built_actions = {}
        actions_data = datahelpers.get_all_from_dir(ACTION_DIR)
        for action in actions_data:
            name = action[0]
            data = action[1]
            a_class = getattr(actions, data["class"])
            i_name = data["i_name"]
            d_name = data["d_name"]
            descriptions = data["descriptions"]
            a_args = data["args"]
            game = self
            built_actions[name] = a_class(i_name, d_name,
                                          descriptions, game, *a_args)
        return built_actions

    def build_world(self, dir):
        data_dict = datahelpers.load_json(dir+"/world.json")
        i_name = data_dict["i_name"]
        d_name = data_dict["d_name"]
        descriptions = data_dict["descriptions"]
        flags = data_dict["flags"]
        parent = self
        rooms = []
        return World(i_name, d_name, descriptions, flags, parent, rooms)

    def build_rooms(self):
        built_rooms = {}
        rooms = datahelpers.get_all_from_dir(ROOM_DIR)
        for room in rooms:
            name = room[0]
            data_dict = room[1]
            i_name = data_dict["i_name"]
            d_name = data_dict["d_name"]
            descriptions = data_dict["descriptions"]
            flags = data_dict["flags"]
            parent = self.world
            actors = data_dict["actors"]
            exits = data_dict["exits"]
            items = data_dict["items"]
            new_room = Room(i_name, d_name, descriptions, flags,
                            parent, actors, exits, items)
            # loading in item objects after room is instantiated
            new_room.items = self.build_items(new_room, new_room.items)
            # loading in actor objects after room is instantiated
            new_room.actors = self.build_actors(new_room, new_room.actors)
            built_rooms[name] = new_room

        return built_rooms

    def build_exits(self):
        for room in self.rooms:
            built_exits = []
            for exit_name in self.rooms[room].exits:
                print(exit_name)
                print(dir(exit_name))
                if type(exit_name) != str:
                    print(exit_name.i_name)
                filename = exit_name + ".json"
                path = os.path.join(EXIT_DIR, filename)
                data = datahelpers.load_json(path)
                i_name = data["i_name"]
                d_name = data["d_name"]
                descriptions = data["descriptions"]
                flags = data["flags"]
                conditions = data["conditions"]
                parent = room
                c_room = self.rooms[data["room"]]
                new_exit = Exit(i_name, d_name, descriptions,
                                flags, parent, c_room, conditions)
                built_exits.append(new_exit)
            self.rooms[room].exits = built_exits

    def build_actors(self, parent, actors):
        built_actors = []
        for new_actor in actors:
            built_actors.append(self.build_actor(ACTOR_DIR, new_actor, parent))
        return built_actors

    def build_actor(self, dir, name, parent):
        filename = name + ".json"
        path = os.path.join(dir, filename)
        actor_data = datahelpers.load_json(path)
        a_class = getattr(actor, actor_data["class"])
        i_name = actor_data["i_name"]
        d_name = actor_data["d_name"]
        descriptions = actor_data["descriptions"]
        flags = actor_data["flags"]
        stats = actor_data["stats"]
        actions = [self.actions[action] for action in actor_data["actions"]]
        inventory = actor_data["inventory"]
        new_actor = a_class(i_name, d_name, descriptions, flags,
                            parent, stats, actions, inventory)
        # loading item objects in inventory after actor object instantiated
        new_actor.inventory = self.build_items(new_actor,
                                               new_actor.inventory)
        if isinstance(new_actor, actor.Player):
            self.pc = new_actor
        return new_actor

    def build_items(self, parent, items):
        built_items = []
        for item in items:
            built_items.append(self.build_item(ITEM_DIR, item, parent))
        return built_items

    def build_item(self, dir, name, parent):
        filename = name + ".json"
        path = os.path.join(dir, filename)
        item_data = datahelpers.load_json(path)
        i_name = item_data["i_name"]
        d_name = item_data["d_name"]
        descriptions = item_data["descriptions"]
        flags = item_data["flags"]
        stats = item_data["stats"]
        action = self.actions[item_data["action"]]
        return Item(i_name, d_name, descriptions, flags, parent, stats, action)


if __name__ == "__main__":
    game = Game()
    for roomname, room in game.world.rooms.items():
        print(roomname)
        print(room.actors)
    game.game_loop()
