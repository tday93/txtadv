from game.baseclasses.flaggable import Flaggable


class Room(Flaggable):

    """ rooms are flaggables that hold actor, item and exit objects
        their parent is the world object """

    def __init__(self, i_name, d_name, descriptions,
                 flags, parent, actors, exits, items, aliases=[]):
        super().__init__(i_name, d_name, descriptions,
                         flags, parent, aliases)
        self.actors = actors
        self.items = items
        self.exits = exits
        self.category = "Room"
