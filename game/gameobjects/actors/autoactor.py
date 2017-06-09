import random
from game.gameobjects.actors import Actor


class AutoActor(Actor):
    """
        an auto actor is an actor that can act autonomously,
        without direct player action
    """

    def __init__(self, i_name, d_name, descriptions, flags,
                 parent, stats, actions, inventory, decision_dict,
                 aliases=[]):
        super().__init__(i_name, d_name, descriptions, flags,
                         parent, stats, actions, inventory, aliases=[])
        self.d_dict = decision_dict

    def do_action(self):
        action, target = self.choose_action()
        self.use_action(action, target)

    def choose_action(self):

        """
            Steps:
                1. Find possible targets:
                        other actors,
                        the room,
                        items?
                2. For each possible action, check conditions of target/self
                    THIS STILL NEEDS TO BE DONE,
                    NEED TO FIND GOOD WAY TO DO THIS
                3. collect all possible actions
                4. choose at random based on weight
        """

        # 1:
        possible_actions = []
        targets = self.get_targets()
        for target in targets:
            for action in self.d_dict["actions"]:
                if all(flag in target.flags for flag in action["flags"]):
                    possible_actions.append({"action": action["action"],
                                             "target": target,
                                             "weight": action["weight"]})
        chosen_action = self.weighted_choice(possible_actions)
        action = self.get_action(chosen_action["action"])
        return action, chosen_action["target"]

    def get_targets(self):
        other_actors = self.parent.actors
        room = [self.parent]
        items = self.inventory

        return other_actors + room + items

    def get_action(self, i_name):
        for action in self.actions:
            if action.i_name == i_name:
                return action

    def weighted_choice(self, possible_actions):
        choice_list = [[action] * action["weight"]
                       for action in possible_actions]

        flat_choice_list = [val for sublist in choice_list for val in sublist]
        return random.choice(flat_choice_list)
