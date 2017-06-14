from game.baseclasses.stattable import Stattable


class Item(Stattable):

    """ items are stattables with a !!!single!!! action attached i
        this action is activated with the USE action by an actor """

    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
        self.action = kw["action"]
        self.category = "Item"

    def use(self, actor, target, **kwargs):
        self.action.do_action(actor, target, **kwargs)
