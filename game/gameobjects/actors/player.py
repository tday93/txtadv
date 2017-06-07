from game.gameobjects.actors.actor import Actor


class Player(Actor):

    """ player character actor
        there should be only one of these in a game
        (for the time being)
    """

    def __init__(self, i_name, d_name, descriptions, flags,
                 parent, stats, actions, inventory, aliases=[]):
        super().__init__(i_name, d_name, descriptions, flags,
                         parent, stats, actions, inventory, aliases)
