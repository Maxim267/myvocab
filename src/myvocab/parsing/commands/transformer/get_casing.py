import logging

from src.myvocab.parsing.vocabulary import vocabulary as vcb
from src.myvocab.constants import constants as cns
from src.myvocab.exceptions import exceptions as exc
from src.myvocab.parsing.commands.transformer.get_init_data import get_init_data
from src.myvocab.utils.str_handler.join_current_target_words import join_current_target_words
from src.myvocab.utils.str_handler.get_priority_word import get_priority_word
from src.myvocab.utils.str_handler.combine_current_target_words import combine_current_target_words

logger = logging.getLogger(__name__)


def check_casing_data(data: dict) -> None:
    """ Check the processed data for identifiers allocated to casing.

    Args:
        data (dict): The input data
    """

    cur_range = cns.RANGE_CASING_ID
    # The range's max_id value must only be accessed outside this function
    cur_range_max_id = cns.RANGE_CASING_MAX_ID

    # In case of design range violation
    if data['id'] not in cur_range:
        raise exc.IdentifierOutOfRangeError(data['id'], cur_range)
    if data['id'] == cur_range_max_id:
        raise exc.IdentifierInvalidValueError(data['id'],
                                              message="The max_id of the range must only be used outside of this function:")


def get_casing_dict(vocab: vcb.VocabConfig, data: dict, case_word: str) -> dict:
    """ Search for the input word in the `casing` dictionary.

    Args:
        vocab (VocabConfig): 'Vocabulary configuration' object
        data (dict): The input data
        case_word (str): The current mixed-case input word
    Returns:
        dict: Processed data
    """
    cur_word = data["word"].lower().strip()
    cur_data = get_init_data(cur_word)
    case_lower = case_word.lower().strip()

    # It requires a word in the mixed_casing list to be equal to the input case_word
    if (mc_list := vocab.casing.mixed_casing.get(case_lower)) and case_word in mc_list:
        cur_data = {
            "id": 2010,
            "word": case_word,
            "pair": ""
        }

    # If data has changed
    if cur_data['id'] != cns.UNCHANGED_DATA_ID:
        # Log the word transformation pair
        logger.debug(f"(id={cur_data['id']}) {case_word[:len(cur_data['word'])]} -> {cur_data['word']}")

        # In case of design range violation
        check_casing_data(cur_data)

        # The word changed into a `casing`
        return cur_data

    # The data has not changed
    return data


def get_casing_form(vocab: vcb.VocabConfig, data: dict, case_word: str) -> dict:
    """ Change the case of a word

    Args:
        vocab (VocabConfig): 'Vocabulary configuration' object
        data (dict): The input data
        case_word (str): The current mixed-case input word
    Returns:
        dict: Processed data
    """

    cur_word = data["word"].lower().strip()
    cur_data = get_init_data(cur_word)
    case_lower = case_word.lower().strip()

    base_word = case_word

    # If the root of the word has been modified (e.g., an irregular word)
    min_length = min(len(case_lower), len(cur_word))
    if case_lower[:min_length] != cur_word[:min_length]:
        base_word = combine_current_target_words(case_word, cur_word)

    # Join the prefix of the current string with the suffix of the target string
    join_word = join_current_target_words(base_word, cur_word)

    # Get the priority string from a list of mixed-case strings
    if val := get_priority_word(vocab.casing.mixed_casing.get(cur_word), join_word):
        cur_data = {
            "id": 2020,
            "word": val,
            "pair": "" if join_word == val else f"{join_word} - {val}"
        }

    # If data has changed
    if cur_data['id'] != cns.UNCHANGED_DATA_ID:
        # Log the word transformation pair
        logger.debug(f"(id={cur_data['id']}) {case_word[:len(cur_data['word'])]} -> {cur_data['word']}")

        # In case of design range violation
        check_casing_data(cur_data)

        # The word changed into a casing
        return cur_data

    return data
