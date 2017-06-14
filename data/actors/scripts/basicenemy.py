"""

    an ai script is a function that gets called
    each round and is what makes the
    autonomous actor do something

    this will be passed the actor object so it will be able to access anything
    the actor could access


    IMPORTANT: this should not actually change the state of anything, it should
    only examine state, and based on that state choose an action/target for the
    actor to perform

"""


def get_script():
    return do_action


def do_action(actor):
    if actor.stats["hp"] <= 0:
        return
    try:
        action = actor.get_action_from_i_name("attack")
        target = actor.get_target("playercharacter")
        actor.use_action(action, target)
    except KeyError as e:
        pass
