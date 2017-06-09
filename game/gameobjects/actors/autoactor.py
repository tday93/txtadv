from game.gameobjects.actors import Actor


class AutoActor(Actor):
    """
        an auto actor is an actor that can act autonomously,
        without direct player action
    """

    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
        self.d_script = kw["d_script"]

    def do_action(self):
        action, target = self.choose_action()
        self.use_action(action, target)
