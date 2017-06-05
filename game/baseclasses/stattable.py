from game.baseclasses.flaggable import Flaggable


class Stattable(Flaggable):

    """ stattable objects have a stats dict in the form:
        {"stat_name":<int>}
        """

    def __init__(self, i_name, d_name, descriptions,
                 flags, parent, stats, aliases=[]):
        super().__init__(i_name, d_name, descriptions, flags, parent, aliases)
        self.stats = stats
