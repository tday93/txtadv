import importlib
import sys
from game.baseclasses.defaultobject import DefaultObject


class Actor(DefaultObject):

    """ actors are stattables tht can use actions
        actors can contain items
        their parent is the current room they are in

        actions = list of object
        inventory = list of item objects
    """

    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
        self.actions = kw["actions"]
        self.inventory = kw["inventory"]
        self.category = "Actor"

    def use_action(self, action, target, **kwargs):
        if action is not None and target is not None:
            if action.i_name in self.actions:
                action.do_action(self, target, **kwargs)

    def is_attackable(self):
        if "hp" in self.stats and "def" in self.stats:
            return True
        return False

    def is_lootable(self):
        if "lootable" in self.flags:
            return True
        return False

    def get_all_targets(self):
        other_actors = self.parent.actors
        room = [self.parent]
        items = self.inventory

        return other_actors + room + items + [self]

    def get_action_from_i_name(self, i_name):
        for action in self.actions:
            if action.i_name == i_name:
                return action

    def get_target(self, i_name):
        for target in self.get_all_targets():
            if target.i_name == i_name:
                return target

    def do_action(self):
        pass

    @staticmethod
    def get_actor(parent, **kw):
        if kw["class"] == "Actor":
            return Actor(parent, **kw)
        elif kw["class"] == "Player":
            return Player(parent, **kw)
        elif kw["class"] == "AutoActor":
            return AutoActor(parent, **kw)


class Player(Actor):

    """ player character actor
        there should be only one of these in a game
        (for the time being)
    """

    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
        # for now, register self as PC
        self.parent.pc = self


class AutoActor(Actor):
    """
        an auto actor is an actor that can act autonomously,
        without direct player action
    """

    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
        self.script_dir = kw["script_dir"]
        self.script_name = kw["script_name"]
        self.load_script()

    def load_script(self):
        sys.path.append(self.script_dir)
        self.script_mod = importlib.import_module(self.script_name)
        self.script = self.script_mod.get_script()

    def do_action(self):
        self.script(self)
