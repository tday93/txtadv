from game.baseclasses.stattable import Stattable


class Actor(Stattable):

    """ actors are stattables tht can use actions
        actors can contain items
        their parent is the current room they are in

        actions = list of object
        inventory = list of item objects
    """

    def __init__(self, i_name, d_name, descriptions, flags,
                 parent, stats, actions, inventory, aliases=[]):
        super().__init__(i_name, d_name, descriptions,
                         flags, parent, stats, aliases)
        self.actions = actions
        self.inventory = inventory
        self.category = "Actor"

    def use_action(self, action, target, use_text):
        if action in self.actions:
            action.do_action(self, target, use_text)

    def is_attackable(self):
        if "hp" in self.stats and "def" in self.stats:
            return True
        return False

    def is_lootable(self):
        if "lootable" in self.flags:
            return True
        return False
