""" this translates the players input into a call to an action


            do_action should take form:
                do_action(self, act-er, target, use_text, *args, **kwargs)


        example player input:

            "move door"
            "use item_name"
            "attack enemy_name"

            Action Target Object
"""


def parse_player_input(game, player, use_text):
    extra = {"use_text": use_text}
    s_text = use_text.split(" ")
    a_name = s_text[0]
    action = get_action(player, a_name)
    if len(s_text) >= 1:
        s_text.append("all")
    if len(s_text) >= 2:
        t_name = s_text[1]
        target = get_target(player, t_name)
    if len(s_text) >= 3:
        s_name = s_text[2]
        subject = get_target(player, s_name)
        extra["subject"] = subject

    return action, target, extra


def get_action(player, a_name):

    actions = [action for action in list(player.parent.actions.values())
               if name_check(a_name, action)]
    if len(actions) == 1:
        return actions[0]


def get_target(player, t_name):
    p_targets = get_possible_targets(player)
    targets = [target for target in p_targets if name_check(t_name, target)]

    if len(targets) == 1:
        return targets[0]
    else:
        return targets


def get_possible_targets(player):
    """
        ALLOWABLE TARGETS:
            Self,
            Other Actors,
            The Room,
            Items,
            Exits,
            Actions?
    """
    other_actors = list(player.parent.actors.values())
    room = list(player.parent.rooms.values())
    items = list(player.parent.items.values())
    actions = list(player.parent.actions.values())

    return other_actors + room + items + actions


def name_check(name, thing):
    checklist = [name == thing.i_name, name == thing.d_name,
                 name in thing.aliases, name == "all"]

    return any(checklist)
