import logging
import re
from src.myvocab.parsing.vocabulary import vocabulary as vcb
from src.myvocab.constants import constants as cns
from src.myvocab.exceptions import exceptions as exc
from src.myvocab.parsing.commands.get_init_data import get_init_data

logger = logging.getLogger(__name__)

def get_infinit(word: str, vocab: vcb.VocabConfig) -> dict:
    """ Convert  a verb to its infinitive form.

    Args:
        word (str): The input word may be modified
        vocab (VocabConfig): 'Vocabulary configuration' object
    Returns:
        dict: Processed data
    """

    cur_range = cns.RANGE_INFINIT_ID
    cur_word = word.lower().strip()
    cur_data = get_init_data(cur_word)

    # It requires an irregular verb in the V3 form
    if verb := vocab.infinit.verbs_v3.get(cur_word):
        cur_data = {
                "id": 1010,
                "word": verb,
                "pair": "" if cur_word == verb else f"{cur_word} - {verb}"
            }
    # It requires an irregular verb in the V2 form
    elif verb := vocab.infinit.verbs_v2.get(cur_word):
        cur_data = {
                "id": 1020,
                "word": verb,
                "pair": "" if cur_word == verb else f"{cur_word} - {verb}"
            }
    # It requires an irregular verb in the V1 form
    elif verb := vocab.infinit.verbs_v1.get(cur_word):
        cur_data = {
                "id": 1030,
                "word": verb,
                "pair": ""
            }
    # It requires a word ending in -ed
    elif cur_word in vocab.infinit.only_ending_ed:
        cur_data = {
            "id": 1040,
            "word": cur_word,
            "pair": ""
        }

    # It requires a verb ending in '-ed'
    elif verb_e_d := re.findall(r'((.+)e)d\b', cur_word):
        # Searching for a verb ending in '-e' in the set
        if verb_e_d[0][0] in vocab.infinit.verbs_ending_e:
            val = verb_e_d[0][0]
            cur_data = {
                "id": 1050,
                "word": val,
                "pair": "" if cur_word == val else f"{cur_word} - {val}"
            }
        # Searching for a verb not ending in '-ed' in the set
        elif verb_e_d[0][1] in vocab.infinit.verbs_ending_non_ed:
            val = verb_e_d[0][1]
            cur_data = {
                "id": 1060,
                "word": val,
                "pair": "" if cur_word == val else f"{cur_word} - {val}"
            }
        # It requires a verb ending in '-ed'
        else:
            try:
                # It requires a verb ending in '2 consonants + ed'
                verb_2consonants_ed = next(re.finditer(r'.+([^aeiouy])\1ed\b', cur_word))
            except Exception:
                verb_2consonants_ed = None
            if not verb_2consonants_ed:
                # It requires a verb ending in 'consonant + -ied'
                verb_ied = re.findall(r'(.+[^aeiouy])ied\b', cur_word)
                if not verb_ied:
                    # It requires a verb ending in '-xed'
                    verb_xed = re.findall(r'(.+x)ed\b', cur_word)
                    if not verb_xed:
                        # It requires a verb ending in '-icked'
                        verb_ic_ked = re.findall(r'(.+ic)ked\b', cur_word)
            # It requires a verb ending in '2 consonants + ed'
            if verb_2consonants_ed:
                # removes the '-ed' ending and reduce any double consonants
                val = verb_2consonants_ed.group()[:verb_2consonants_ed.end() - 3]
                cur_data = {
                    "id": 1070,
                    "word": val,
                    "pair": "" if cur_word == val else f"{cur_word} - {val}"
                }
            # It requires a verb ending in 'consonant + -ied'
            elif verb_ied:
                # removes the '-ed' ending and replaces 'i' with 'y'
                val = verb_ied[0] + "y"
                cur_data = {
                    "id": 1080,
                    "word": val,
                    "pair": "" if cur_word == val else f"{cur_word} - {val}"
                }
            # It requires a verb ending in '-xed'
            elif verb_xed:
                # removes the '-ed' ending
                val = verb_xed[0]
                cur_data = {
                    "id": 1090,
                    "word": val,
                    "pair": "" if cur_word == val else f"{cur_word} - {val}"
                }
            # It requires a verb ending in '-icked'
            elif verb_ic_ked:
                # removes the '-ked' ending
                val = verb_ic_ked[0]
                cur_data = {
                    "id": 1100,
                    "word": val,
                    "pair": "" if cur_word == val else f"{cur_word} - {val}"
                }
            # It requires a verb ending in '-ed'
            else:
                # removes the '-ed' ending
                val = verb_e_d[0][1]
                cur_data = {
                    "id": 1110,
                    "word": val,
                    "pair": "" if cur_word == val else f"{cur_word} - {val}"
                }

    # If data has changed
    if cur_data['id'] != cns.UNCHANGED_DATA_ID:
        # Log the word transformation pair
        logger.debug(f"(id={cur_data['id']}) {cur_word} -> {cur_data['word']}")
        # In case of design range violation
        if cur_data['id'] not in cur_range:
            raise exc.IdentifierOutOfRangeError(cur_data['id'], cur_range)

    return cur_data