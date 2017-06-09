from game.baseclasses.flaggable import Flaggable


class World(Flaggable):
    """ the world object holds all rooms, and global flags
        its parent is the game object """

    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
        self.rooms = kw["rooms"]
        self.category = "World"

    def get_room(self, room_name):
        """ get a room object based on its name """
        for room in self.rooms:
            if room_name == room.i_name:
                return room

    # override get_flags method from Flaggable to keep it from asking game
    def get_flags(self):
        return self.flags
