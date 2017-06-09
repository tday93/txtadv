

def check_conditions(conditions, *args):
    """ checks if list of conditions is satisfied """

    if conditions == []:
        """ empty list means no conditions need to be met, so return true """
        return True
    return all(any(flag in item.get_flags() for item in args) for flag in conditions)

