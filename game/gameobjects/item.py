from game.baseclasses.stattable import Stattable


class Item(Stattable):

    """ items are stattables with a !!!single!!! action attached i
        this action is activated with the USE action by an actor """

    def __init__(self, i_name, d_name, descriptions,
                 flags, parent, stats, action, aliases=[]):
        super().__init__(i_name, d_name, descriptions,
                         flags, parent, stats, aliases)
        self.action = action
        self.category = "Item"

    def use(self, actor, use_text):
        self.action.do_action(actor, use_text)
