from game.helpers.helpers import check_conditions
from game.baseclasses.flaggable import Flaggable


class Exit(Flaggable):

    """ an exit is a path to a room
        exits are only visible/usable if certain conditions are met
        conditions take the form:
            {jjjjjjj}

        self.room = the room that this exit connects to
    """

    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
        self.room = kw["c_room"]
        self.conditions = kw["conditions"]
        self.category = "Exit"

    def usable(self, actor):
        return check_conditions(self.conditions["usable"], self, actor)

    def visible(self, actor):
        return check_conditions(self.conditions["visible"], self, actor)
