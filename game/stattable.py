from game.flaggable import Flaggable


class Stattable(Flaggable):

    """ stattable objects have a stats dict in the form:
        {"stat_name":<int>}
        """

    def __init__(self, i_name, d_name, descriptions, flags, parent, stats):
        super().__init__(i_name, d_name, descriptions, flags, parent)
        self.stats = stats
