from game.gameobjects.actors.actor import Actor


class Room(Actor):

    """ rooms are actors that hold other actors, item and exit objects
        their parent is the world object """

    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
        self.category = "Room"
        self.g_actors = [parent.get_actor(actor) for actor in self.actors]
