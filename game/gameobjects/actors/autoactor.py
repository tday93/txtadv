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
        self.decision_dict = decision_dict

    def do_action(self):
        pass


    def choose_action(self):
        
        """
            Steps:
                1. Find possible targets:
                        other actors,
                        the room,
                        items?
                2. For each possible action, check conditions of target/self
                3. collect all possible actions
                4. choose at random based on weight
        """

        # 1:
        targets = self.get_targets()


    def get_targets(self):
        other_actors = self.parent.actors
        room = [self.parent]
        items = self.inventory

        return other_actors + room + items



