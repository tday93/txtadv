from game.baseclasses.describable import Describable


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

    '''

    def __init__(self, i_name, d_name, descriptions, game, *args):
        super().__init__(i_name, d_name, descriptions)
        self.game = game
        self.category = "Action"

    def do_action(self, actor, use_text):
        pass


class TestAction(Action):

    def __init__(self, i_name, d_name, descriptions, game, *args):
        super().__init__(i_name, d_name, descriptions, game, *args)

    def do_action(self, actor, use_text):
        self.game.output_text("This is the test action")
        self.game.output_text("You said: '{}'".format(use_text))


class Move(Action):

    """ moves an actor through an exit, if exit is usable """

    def __init__(self, i_name, d_name, descriptions, game, *args):
        super().__init__(i_name, d_name, descriptions, game, *args)

    def do_action(self, actor, use_text):
        s_text = use_text.split(" ", 1)
        t_d_name = s_text[1]
        current_room = actor.parent
        exit = self.get_exit(actor, t_d_name)
        if exit:
            current_room.actors.remove(actor)
            actor.parent = exit.room
            exit.room.actors.append(actor)

    def get_exit(self, actor, t_d_name):
        for exit in actor.parent.exits:
            if t_d_name == exit.d_name:
                if exit.usable(actor):
                    return exit
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

    def do_action(self, actor, use_text):
        s_text = use_text.split(" ", 1)
        t_name = s_text[1]
        examinables = self.get_examinables(actor)
        for item in examinables:
            if t_name == item.d_name or t_name == item.i_name or t_name == "all":
                description = item.describe(actor)
                # send text out
                self.game.output_text(description)

    def get_examinables(self, actor):
        actions = actor.actions
        items = actor.inventory
        room = [actor.parent]
        exits = actor.parent.exits
        actors = actor.parent.actors
        return items + room + exits + actors + actions


class Use(Action):

    """ use an items attached action """

    def __init__(self, i_name, d_name, descriptions, game, *args):
        super().__init__(i_name, d_name, descriptions, game, *args)

    def do_action(self, actor, use_text):
        s_text = use_text.split(" ", 1)
        item_name = s_text[1]
        for item in actor.inventory:
            if item_name.startswith(item.i_name) or item_name.startswith(item.d_name):
                item.use(actor, use_text)
