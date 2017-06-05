import os
from game.helpers import datahelpers
from game.actions import actions
from game.gameobjects import actor
from game.gameobjects import player
from game.gameobjects.world import World
from game.gameobjects.room import Room
from game.gameobjects.item import Item
from game.gameobjects.exit import Exit


def build_actions(game):
    action_dir = game.base_dir + "/actions"
    built_actions = {}
    actions_data = datahelpers.get_all_from_dir(action_dir)
    for action in actions_data:
        name = action[0]
        data = action[1]
        a_class = getattr(actions, data["class"])
        i_name = data["i_name"]
        d_name = data["d_name"]
        descriptions = data["descriptions"]
        a_args = data["args"]
        built_actions[name] = a_class(i_name, d_name,
                                      descriptions, game, *a_args)
    return built_actions


def build_world(game):
    world_file = game.base_dir + "/world.json"
    data_dict = datahelpers.load_json(world_file)
    i_name = data_dict["i_name"]
    d_name = data_dict["d_name"]
    descriptions = data_dict["descriptions"]
    flags = data_dict["flags"]
    parent = game
    rooms = []
    aliases = data_dict["aliases"]
    return World(i_name, d_name, descriptions, flags, parent, rooms, aliases)


def build_rooms(game):
    room_dir = game.base_dir + "/rooms"
    built_rooms = {}
    rooms = datahelpers.get_all_from_dir(room_dir)
    for room in rooms:
        name = room[0]
        data_dict = room[1]
        i_name = data_dict["i_name"]
        d_name = data_dict["d_name"]
        descriptions = data_dict["descriptions"]
        flags = data_dict["flags"]
        parent = game.world
        actors = data_dict["actors"]
        exits = data_dict["exits"]
        items = data_dict["items"]
        aliases = data_dict["aliases"]
        new_room = Room(i_name, d_name, descriptions, flags,
                        parent, actors, exits, items, aliases)
        # loading in item objects after room is instantiated
        new_room.items = build_items(game, new_room, new_room.items)
        # loading in actor objects after room is instantiated
        new_room.actors = build_actors(game, new_room, new_room.actors)
        built_rooms[name] = new_room

    return built_rooms


def build_exits(game):
    exit_dir = game.base_dir + "/exits"
    for room in game.rooms:
        built_exits = []
        for exit_data in game.rooms[room].exits:
            exit_name = exit_data["exit"]
            filename = exit_name + ".json"
            path = os.path.join(exit_dir, filename)
            data = datahelpers.load_json(path)
            i_name = data["i_name"]
            d_name = data["d_name"]
            descriptions = data["descriptions"]
            flags = data["flags"]
            conditions = data["conditions"]
            parent = room
            c_room = game.rooms[exit_data["room"]]
            aliases = data["aliases"]
            new_exit = Exit(i_name, d_name, descriptions,
                            flags, parent, c_room, conditions, aliases)
            built_exits.append(new_exit)
        game.rooms[room].exits = built_exits


def build_actors(game, parent, actors):
    actor_dir = game.base_dir + "/actors"
    built_actors = []
    for new_actor in actors:
        built_actors.append(build_actor(game, actor_dir, new_actor, parent))
    return built_actors


def build_actor(game, dir, name, parent):
    filename = name + ".json"
    path = os.path.join(dir, filename)
    data_dict = datahelpers.load_json(path)
    if data_dict["class"] == "Player":
        a_class = getattr(player, data_dict["class"])
    else:
        a_class = getattr(actor, data_dict["class"])
    i_name = data_dict["i_name"]
    d_name = data_dict["d_name"]
    descriptions = data_dict["descriptions"]
    flags = data_dict["flags"]
    stats = data_dict["stats"]
    actions = [game.actions[action] for action in data_dict["actions"]]
    inventory = data_dict["inventory"]
    aliases = data_dict["aliases"]
    new_actor = a_class(i_name, d_name, descriptions, flags,
                        parent, stats, actions, inventory, aliases)
    # loading item objects in inventory after actor object instantiated
    new_actor.inventory = build_items(game, new_actor,
                                      new_actor.inventory)
    if isinstance(new_actor, player.Player):
        game.pc = new_actor
    return new_actor


def build_items(game, parent, items):
    item_dir = game.base_dir + "/items"
    built_items = []
    for item in items:
        built_items.append(build_item(game, item_dir, item, parent))
    return built_items


def build_item(game, dir, name, parent):
    filename = name + ".json"
    path = os.path.join(dir, filename)
    data_dict = datahelpers.load_json(path)
    i_name = data_dict["i_name"]
    d_name = data_dict["d_name"]
    descriptions = data_dict["descriptions"]
    flags = data_dict["flags"]
    stats = data_dict["stats"]
    action = game.actions[data_dict["action"]]
    aliases = data_dict["aliases"]
    return Item(i_name, d_name, descriptions, flags,
                parent, stats, action, aliases)