from src.myvocab.constants import constants as cns

def get_init_data(word: str=""):
    """ Initializing data.

    Args:
        word (str): The input word.
    Returns:
        dict: Initial data with 'id', 'word', and 'pair' fields.
    """

    return {"id": cns.UNCHANGED_DATA_ID, "word": word, "pair": ""}