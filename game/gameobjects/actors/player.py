from game.gameobjects.actors.actor import Actor


class Player(Actor):

    """ player character actor
        there should be only one of these in a game
        (for the time being)
    """

    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
