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

    action = actor.get_action("move")
    target = actor.get_target("door")
    extra_arg = "boop"

    actor.use_action(action, target, exta_arg=extra_arg)
