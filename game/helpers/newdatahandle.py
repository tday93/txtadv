from game.helpers import datahelpers
from game.actions import actions
from game.gameobjects.actors.actor import Actor
from game.gameobjects.world import World
from game.gameobjects.room import Room
from game.gameobjects.item import Item
from game.gameobjects.exit import Exit


"""

GOALS:
    EVERY OBJECT IS FLAT
    EVERY OBJECT HOLDS ITS LOCATION


Game
    World
        Room
            Exit
            Actor
                Item
            Item


i_name
d_name
descriptions
flags
exits
inventory
stats
actions
aliases


"""


def build_actions(game):
    action_dir = game.base_dir + "/actions"
    built_actions = {}
    actions_data = datahelpers.get_all_from_dir(action_dir)
    for action in actions_data:
        name = action[0]
        data = action[1]
        built_actions[name] = actions.Action.get_action(game, **data)
    return built_actions


def build_world(game):
    world_file = game.base_dir + "/world.json"
    data = datahelpers.load_json(world_file)
    return World(game, **data)


def build_rooms(game):
    room_dir = game.base_dir + "/rooms"
    built_rooms = {}
    rooms = datahelpers.get_all_from_dir(room_dir)
    for room in rooms:
        name = room[0]
        data = room[1]
        new_room = Room(game, **data)
        new_room.g_exits = build_exits(new_room, new_room.exits)
        built_rooms[name] = new_room

    return built_rooms


def build_exits(room, exits):
    built_exits = {}
    for exit in exits:
        print(exit)
        name = exit["i_name"]
        data = exit
        new_exit = Exit(room, **data)
        built_exits[name] = new_exit

    return built_exits


def build_actors(game):
    actor_dir = game.base_dir + "/actors"
    built_actors = {}
    actors = datahelpers.get_all_from_dir(actor_dir)
    for actor in actors:
        name = actor[0]
        data = actor[1]
        data["script_dir"] = actor_dir + "/scripts"
        new_actor = Actor.get_actor(game, **data)
        built_actors[name] = new_actor

    return built_actors


def build_items(game):
    item_dir = game.base_dir + "/items"
    built_items = {}
    items = datahelpers.get_all_from_dir(item_dir)
    for item in items:
        name = item[0]
        data = item[1]
        new_item = Item(game, **data)
        built_items[name] = new_item

    return built_items
