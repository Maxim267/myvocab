import re

def get_verbs_s(verbs: dict) -> set:
    """ Get verbs ending in '-s' from the map keys.

    Args:
        verbs (dict): Map with verbs as keys.
    Returns:
        set: Keys of the map ending in '-s'.
    """

    out_verbs = set()
    for verb in verbs.keys():
        if re.findall(r'.+s\b', verb):
            out_verbs.add(verb)
    return out_verbs