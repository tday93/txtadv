from game.helpers.helpers import check_conditions


class Describable(object):

    '''Base class for anything that needs to be described
        Describables have a list of dicts of form:
            {"flags":["flags"],"description":"description"}

        They also have a reference to their parent object for convenience
        in referencing the state of that parent '''

    def __init__(self, **kw):
        self.i_name = kw["i_name"]
        self.d_name = kw["d_name"]
        self.category = "Describable"
        self.descriptions = kw["descriptions"]
        self.aliases = kw["aliases"]

    def describe(self, actor):
        """ get the descriptions of this object,
            based on the state of the actor """
        desc_out = []
        for desc in self.descriptions:
            if check_conditions(desc["flags"], actor.get_flags()):
                desc_out.append(desc["description"])
        if desc_out:
            desc_out = " ".join(desc_out)
            desc_out = "({}) {} : {}".format(self.category,
                                             self.d_name, desc_out)

        return desc_out
