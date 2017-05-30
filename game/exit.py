from helpers import check_conditions
from flaggable import Flaggable


class Exit(Flaggable):

    """ an exit is a path to a room
        exits are only visible/usable if certain conditions are met
        conditions take the form:
            {"usable":["list","of","flags"], "visible":["list", "of", "flags"]}

        self.room = the room that this exit connects to
    """

    def __init__(self, i_name, d_name, descriptions,
                 flags, parent, c_room, conditions):
        super().__init__(i_name, d_name, descriptions, flags, parent)
        self.room = c_room
        self.conditions = conditions
        self.category = "Exit"

    def usable(self, actor):
        return check_conditions(self.conditions["usable"], self, actor)

    def visible(self, actor):
        return check_conditions(self.conditions["visible"], self, actor)
