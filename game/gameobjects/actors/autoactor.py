import importlib
from game.gameobjects.actors.actor import Actor


class AutoActor(Actor):
    """
        an auto actor is an actor that can act autonomously,
        without direct player action
    """

    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
        self.script_dir = kw["script_dir"]
        self.script_name = kw["script_name"]
        self.load_script()

    def load_script(self):
        self.script_mod = importlib.import_module(self.script_name)
        self.script = self.script_mod.get_script()

    def do_action(self):
        self.script(self)
