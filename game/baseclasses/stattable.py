from game.baseclasses.flaggable import Flaggable


class Stattable(Flaggable):

    """ stattable objects have a stats dict in the form:
        {"stat_name":<int>}
        """

    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
        self.stats = kw["stats"]
