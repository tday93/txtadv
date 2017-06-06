from game.gameobjects.actor import Actor


class Room(Actor):

    """ rooms are actors that hold other actors, item and exit objects
        their parent is the world object """

    def __init__(self, i_name, d_name, descriptions, flags,
                 parent, stats, actions, inventory, actors, exits, aliases=[]):
        super().__init__(i_name, d_name, descriptions, flags,
                         parent, stats, actions, inventory, aliases=[])
        self.actors = actors
        self.exits = exits
        self.category = "Room"
