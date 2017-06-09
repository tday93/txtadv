from game.gameobjects.exit import Exit
from game.baseclasses.describable import Describable
from game.gameobjects.actors.actor import Actor
from game.gameobjects.item import Item


class Action(Describable):

    ''' actions are the only things that can mutate game state

        they are describable but do not change state,
        an action object will always
        do the exact same thing each time

        they are invoked with the form:

            VERB SUBJECT [on/with/filler] OBJECT

            "use sword on spider"
            "go (Wooden Door)"
            "examine room"

        REWRITE:

            this needs to be re-done to account for non-player actors
                ie, they shouldn't have to build use-text

            do_action should take form:
                do_action(self, act-er, target, *args, **kwargs)

        ALLOWABLE TARGETS:
            Self,
            Other Actors,
            The Room,
            Items,
            Exits,
            Actions?

    '''

    def __init__(self, i_name, d_name, descriptions, game, *args):
        super().__init__(i_name, d_name, descriptions)
        self.game = game
        self.category = "Action"

    def do_action(self, actor, target, **kwargs):
        pass


class TestAction(Action):

    def __init__(self, i_name, d_name, descriptions, game, *args):
        super().__init__(i_name, d_name, descriptions, game, *args)

    def do_action(self, actor, target, **kwargs):
        self.game.output_text("This is the test action")
        self.game.output_text("You said: '{}'".format(kwargs["use_text"]))
        self.game.output_text("kwargs are:")
        for k, v in kwargs.items():
            self.game.output_text("{} : {}".format(k, v))


class Move(Action):

    """ moves an actor through an exit, if exit is usable """

    def __init__(self, i_name, d_name, descriptions, game, *args):
        super().__init__(i_name, d_name, descriptions, game, *args)

    def do_action(self, actor, target, **kwargs):
        current_room = actor.parent
        if isinstance(target, Exit) and target.usable(actor):
            current_room.actors.remove(actor)
            actor.parent = target.room
            target.room.actors.append(actor)

        return None


class Examine(Action):

    """ gets the description of a given object

        scope for this check is:
            items in actors inventory
            the room itself
            exits in current room
            actors in current room
            actions the player has

    """

    def __init__(self, i_name, d_name, descriptions, game, *args):
        super().__init__(i_name, d_name, descriptions, game, *args)

    def do_action(self, actor, target, **kwargs):

        if isinstance(target, Describable):
            description = target.describe(actor)
            self.game.output_text(description)
        elif isinstance(target, list):
            for item in target:
                if isinstance(item, Describable):
                    description = item.describe(actor)
                    self.game.output_text(description)


class Use(Action):

    """ use an items attached action """

    def __init__(self, i_name, d_name, descriptions, game, *args):
        super().__init__(i_name, d_name, descriptions, game, *args)

    def do_action(self, actor, target, **kwargs):
        if isinstance(target, Item):
                target.use(actor, target, **kwargs)


class Attack(Action):

    def __init__(self, i_name, d_name, descriptions, game, *args):
        super().__init__(i_name, d_name, descriptions, game, *args)

    def do_action(self, actor, target, **kwargs):

        if isinstance(target, Actor) and target.is_attackable():
            self.combat_calc(actor, target)

    def combat_calc(self, attacker, defender):
        if not defender.is_attackable():
            self.game.output_text(
                "{} is not attackable".format(defender.d_name))
        a_atk = attacker.stats["atk"]
        d_def = defender.stats["def"]
        dmg = a_atk - d_def
        if dmg > 0:
            defender.stats["hp"] = defender.stats["hp"] - dmg
            self.game.output_text(
                "You do {} damage to the {}".format(dmg, defender.d_name))
            if defender.stats["hp"] >= 0:
                self.game.output_text(
                    "You murdered the {}".format(defender.d_name))
                defender.flags.append("lootable")
        else:
            msg = "You are too weak to hurt the {}".format(defender.d_name)
            self.game.output_text(msg)


class Get(Action):
    """ transfer an item from one actors inventory to another """

    def __init__(self, i_name, d_name, descriptions, game, *args):
        super().__init__(i_name, d_name, descriptions, game, *args)

    def do_actions(self, actor, target, **kwargs):
        pass
