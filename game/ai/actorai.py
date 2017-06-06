""" this is what will make decisions for any given actor

    it sits between the game and the actor and decides what
    action the actor will use, based on defined conditions
"""

class ActorAI(object):

    def __init__(self, actor, decision_dict):

        self.actor = actor
        self.decision_dict = decision_dict


    def actor_check(self, actor, conditions):
        results = []
        for attr, check_vals in conditions.items():
            actor_vals = getattr(actor, attr)
            if isinstance(check_vals, dict):
                results.append(self.dict_check(actor_vals, check_vals))
            if isinstance(check_vals, list):
                results.append(self.list_check(actor_vals, check_vals))
            else:
                results.append(check_vals == actor_vals)
        return all(results)

    def check_actors(self, conditions):
        actors = self.actor.parent.actors
        return any(self.actor_check(actor, conditions) for actor in actors)

    
    def check_room(self, conditions):
        room = self.actor.parent
        return actor_check(room, conditions)

    def dict_check(self, d1, d2):
        try:
            return all( d1[k] >= v for k,v in d2.items())
        except KeyError:
            return False

    def list_check(self, l1, l2):
        return all( item in l2 for item in l1)

    def build_options(self):
        options = []
        for action in self.decision_dict["actions"]:

        pass

