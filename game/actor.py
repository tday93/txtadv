from game.stattable import Stattable


class Actor(Stattable):

    """ actors are stattables tht can use actions
        actors can contain items
        their parent is the current room they are in

        actions = list of object
        inventory = list of item objects
    """

    def __init__(self, i_name, d_name, descriptions, flags,
                 parent, stats, actions, inventory):
        super().__init__(i_name, d_name, descriptions, flags, parent, stats)
        self.actions = actions
        self.inventory = inventory
        self.category = "Actor"

    def use_action(self, action_i_name, use_text):
        for action in self.actions:
            if action_i_name == action.i_name:
                action.do_action(self, use_text)


class Player(Actor):

    """ player character actor
        there should be only one of these in a game
        (for the time being)
    """

    def __init__(self, i_name, d_name, descriptions, flags,
                 parent, stats, actions, inventory):
        super().__init__(i_name, d_name, descriptions, flags,
                         parent, stats, actions, inventory)
