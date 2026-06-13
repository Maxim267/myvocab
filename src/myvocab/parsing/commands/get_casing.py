import logging

from src.myvocab.parsing.vocabulary import vocabulary as vcb
from src.myvocab.constants import constants as cns
from src.myvocab.exceptions import exceptions as exc
from src.myvocab.parsing.commands.get_init_data import get_init_data
from src.myvocab.utils.str_handler.join_current_target_words import join_current_target_words
from src.myvocab.utils.str_handler.get_priority_word import get_priority_word

logger = logging.getLogger(__name__)

def get_casing(vocab: vcb.VocabConfig, case_word: str, key_word: str) -> dict:
    """ Convert a word to case

    Args:
        case_word (str): The current mixed-case input word
        key_word (str): The processed lowercase input word
        vocab (VocabConfig): 'Vocabulary configuration' object
        payload (dict): The processed input payload
    Returns:
        dict: Processed data
    """

    cur_range = cns.RANGE_CASING_ID
    # The range's max_id value must only be accessed outside this function
    cur_range_max_id = cns.RANGE_CASING_MAX_ID
    cur_data = get_init_data(key_word)

    # It requires a word in the mixed_casing list to be equal to the input case_word
    if (mc_list := vocab.casing.mixed_casing.get(case_word.lower())) and case_word in mc_list:
        cur_data = {
            "id": 2010,
            "word": case_word,
            "pair": ""
        }
    else:
        # Join the prefix of the current string with the suffix of the target string
        join_word = join_current_target_words(case_word, key_word)

        # Get the priority string from a list of mixed-case strings
        if val := get_priority_word(vocab.casing.mixed_casing.get(key_word), join_word):
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
        if cur_data['id'] not in cur_range:
            raise exc.IdentifierOutOfRangeError(cur_data['id'], cur_range)
        elif cur_data['id'] == cur_range_max_id:
            raise exc.IdentifierInvalidValueError(cur_data['id'], message = "The max_id of the range must only be used outside of this function:")

    return cur_data

def log_casing(payload: dict, changed: str) -> None:
    # If data has changed
    if payload['id'] != cns.UNCHANGED_DATA_ID:
        # Log the word transformation pair
        logger.debug(f"(id={payload['id']}) {changed}")
        # In case of design range violation
        if payload['id'] not in cns.RANGE_CASING_ID:
            raise exc.IdentifierOutOfRangeError(payload['id'], cns.RANGE_CASING_ID)