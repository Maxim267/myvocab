from src.myvocab.constants import constants as cns


def get_init_data(word: str = "", idn: int = cns.UNCHANGED_DATA_ID) -> dict:
    """ Initializing data.

    Args:
        word (str): The input word.
        idn (int): The input identifier.
    Returns:
        dict: Initial data with 'id', 'word', and 'pair' fields.
    """

    return {"id": idn, "word": word, "pair": ""}


def get_init_infinit_data(word: str = "") -> dict:
    """ Initializing `infinit` data.

    Args:
        word (str): The input word.
    Returns:
        dict: Initial `infinit` data with 'id', 'word', and 'pair' fields.
    """

    return get_init_data(word, cns.RANGE_INFINIT_MAX_ID)


def get_init_singular_data(word: str = "") -> dict:
    """ Initializing `singular` data.

    Args:
        word (str): The input word.
    Returns:
        dict: Initial `singular` data with 'id', 'word', and 'pair' fields.
    """

    return get_init_data(word, cns.RANGE_SINGULAR_MAX_ID)


def get_init_casing_data(word: str = "") -> dict:
    """ Initializing `casing` data.

    Args:
        word (str): The input word.
    Returns:
        dict: Initial `casing` data with 'id', 'word', and 'pair' fields.
    """

    return get_init_data(word, cns.RANGE_CASING_MAX_ID)
