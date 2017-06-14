import os
import sys
from game.helpers import datahelpers
from game.actions import actions
from game.gameobjects.actors import actor
from game.gameobjects.actors import player
from game.gameobjects.actors import autoactor
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
        built_actions[name] = a_class(game, **data)
    return built_actions


def build_world(game):
    world_file = game.base_dir + "/world.json"
    data = datahelpers.load_json(world_file)
    parent = game
    return World(parent, **data)


def build_rooms(game):
    room_dir = game.base_dir + "/rooms"
    built_rooms = {}
    rooms = datahelpers.get_all_from_dir(room_dir)
    for room in rooms:
        name = room[0]
        data = room[1]
        parent = game.world
        new_room = Room(parent, **data)
        # loading in item objects after room is instantiated
        new_room.items = build_items(game, new_room, new_room.inventory)
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
            parent = room
            c_room = game.rooms[exit_data["room"]]
            new_exit = Exit(parent=parent, c_room=c_room, **data)
            built_exits.append(new_exit)
        game.rooms[room].exits = built_exits


def build_actors(game, parent, actors):
    actor_dir = game.base_dir + "/actors"
    sys.path.append(actor_dir + "/scripts")
    built_actors = []
    for new_actor in actors:
        built_actors.append(build_actor(game, actor_dir, new_actor, parent))
    return built_actors


def build_actor(game, dir, name, parent):
    filename = name + ".json"
    path = os.path.join(dir, filename)
    data = datahelpers.load_json(path)
    if data["class"] == "Player":
        a_class = getattr(player, data["class"])
    elif data["class"] == "AutoActor":
        a_class = getattr(autoactor, data["class"])
    else:
        a_class = getattr(actor, data["class"])
    data["script_dir"] = dir + "/scripts"
    data["actions"] = [game.actions[action] for action in data["actions"]]
    new_actor = a_class(parent, **data)
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
    data = datahelpers.load_json(path)
    data["action"] = game.actions[data["action"]]
    return Item(parent, **data)
