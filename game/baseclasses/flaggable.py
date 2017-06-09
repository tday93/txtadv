from game.baseclasses.describable import Describable


class Flaggable(Describable):
    """ anything that can have flags applied to it
        Flaggables are always nouns, and always have a parent """

    def __init__(self, parent, **kw):
        super().__init__(**kw)
        self.flags = kw["flags"]
        self.parent = parent

    def get_flags(self):
        """ get the flags from self and parent """
        return self.flags + self.parent.get_flags()
