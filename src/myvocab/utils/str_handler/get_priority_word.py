def get_priority_word(words: list, word: str) -> str | None:
    """ Get the string with the maximum weight from the list derived from the given word.

    Args:
        words (list): List of words.
        word (str): Word to get the maximum weight from.
    Returns:
        The highest-priority word in the list
    """

    if not words:
        return None

    return_val = ""
    weight = 0
    length = len(word)

    for cur_word in words:
        cur_weight = 0
        # Search priority by word
        index = 0
        for char1, char2 in zip(word, cur_word):
            if char1 == char2:
                cur_weight = cur_weight + (length - int(index)) * (length - int(index))
            index = index + 1
        if cur_weight > weight:
            weight = cur_weight
            return_val = cur_word
        # Otherwise, priority defaults to the first word in the list
        if return_val == "":
            return_val = cur_word

    return return_val