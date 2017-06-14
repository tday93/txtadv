from game.baseclasses.stattable import Stattable


class Actor(Stattable):

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
            if action in self.actions:
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
