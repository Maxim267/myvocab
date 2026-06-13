def combine_current_target_words(current_word: str, target_word: str) -> str:
    """
     Apply the casing from the current character to the target character
     and append the rest of the target word
     """
    length = 0
    new_word = ""
    for curr, targ in zip(current_word, target_word):
        # Match the casing of the target character to the current character
        if curr.isupper():
            new_word += targ.upper()
        else:
            new_word += targ.lower()
        length += 1
    # Append the rest of the target word
    return new_word[:length] + target_word[length:]