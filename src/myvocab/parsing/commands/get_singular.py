import logging
import re
from src.myvocab.parsing.vocabulary import vocabulary as vcb
from src.myvocab.constants import constants as cns
from src.myvocab.exceptions import exceptions as exc
from src.myvocab.parsing.commands.get_init_data import get_init_data

logger = logging.getLogger(__name__)

# Singularize a word
def get_singular(word: str, vocab: vcb.VocabConfig) -> dict:
    """ Convert a word to its singular form.

    Args:
        word (str): The input word may be modified
        vocab (VocabConfig): 'Vocabulary configuration' object
    Returns:
        dict: Processed data
    """

    cur_range = cns.RANGE_SINGULAR_ID
    cur_word = word.lower().strip()
    cur_data = get_init_data(cur_word)

    # It requires an irregular plural noun (e.g., feet)
    if val := vocab.singular.irregular_plural_nouns.get(cur_word):
        cur_data = {
            "id": 10, 
            "word": val, # (e.g., foot)
            "pair": "" if cur_word == val else f"{cur_word} - {val}"
        }
    # It requires a word ending in -s
    elif word_s := re.findall(r'(.+)s\b', cur_word):

        # Searching for a word  with invariable '-s' endings in the set
        if cur_word in vocab.singular.only_ending_s:
            cur_data = {
                "id": 20,
                "word": cur_word,
                "pair": ""
            }
        # Skip further processing for words whose base form does not end in '-s' if they are present in the set.
        elif word_s[0] in vocab.singular.singular_ending_non_s:
            val = word_s[0]
            cur_data = {
                "id": 30,
                "word": val,
                "pair": cur_word + " - " + val
            }
        else:
            # It requires a word ending in -ves
            word_ves = re.findall(r'(.+)ves\b', cur_word)
            if not word_ves:
                # It requires a word ending in 'consonant + o + es|s'
                word_o_es_s = re.findall(r'(.+[^aeiouy]o)(es|s)\b', cur_word)
                if not word_o_es_s:
                    # It requires a word ending in 'consonant + ies'
                    word_ies = re.findall(r'(.+[^aeiouy])ies\b', cur_word)
                    if not word_ies:
                        # It requires a word ending in 'vowel + ys'
                        word_ys = re.findall(r'(.+[aeiouy]y)s\b', cur_word)
                        if not word_ys:
                            # It requires a word ending in 's|ss|ch|sh|x|z + es'
                            word_es = re.findall(r'(.+(s|ss|ch|sh|x|z))es\b', cur_word)
                            if not word_es:
                                # The alphanumeric string ends with 's' (like '1980s')
                                word_09 = re.findall(r'.+[0-9]+s\b', cur_word)

            # Replace '-ves' with '-fe' and look up in the set
            if word_ves and word_ves[0] + 'fe' in vocab.singular.singular_ending_non_s:
                val = word_ves[0] + 'fe'
                cur_data = {
                    "id": 40,
                    "word": val,
                    "pair": cur_word + " - " + val
                }
            # Replace '-ves' with '-f' and look up in the set
            elif word_ves and word_ves[0] + 'f' in vocab.singular.singular_ending_non_s:
                val = word_ves[0] + 'f'
                cur_data = {
                    "id": 50,
                    "word": val,
                    "pair": cur_word + " - " + val
                }
            # Replace '-ves' with '-f'
            elif word_ves:
                val = word_ves[0] + 'f'
                cur_data = {
                    "id": 60,
                    "word": val,
                    "pair": cur_word + " - " + val
                }
            # Removes '-es|s' and look up in the set
            elif word_o_es_s and word_o_es_s[0][0] in vocab.singular.singular_ending_non_s:
                val = word_o_es_s[0][0]
                cur_data = {
                    "id": 70,
                    "word": val,
                    "pair": cur_word + " - " + val
                }
            # Removes '-es|s'
            elif word_o_es_s:
                val = word_o_es_s[0][0]
                cur_data = {
                    "id":80,
                    "word": val,
                    "pair": cur_word + " - " + val
                }
            # Replace '-ies' with '-y' and look up in the set
            elif word_ies and word_ies[0] in vocab.singular.singular_ending_non_s:
                val = word_ies[0] + 'y'
                cur_data = {
                    "id": 90,
                    "word": val,
                    "pair": cur_word + " - " + val
                }
            # Replace '-ies' with '-y'
            elif word_ies:
                val = word_ies[0] + 'y'
                cur_data = {
                    "id": 100,
                    "word": val,
                    "pair": cur_word + " - " + val
                }
            # Removes '-s' and look up in the set
            elif word_ys and word_ys[0] in vocab.singular.singular_ending_non_s:
                val = word_ys[0]
                cur_data = {
                    "id": 110,
                    "word": val,
                    "pair": cur_word + " - " + val
                }
            # Removes '-s'
            elif word_ys:
                val = word_ys[0]
                cur_data = {
                    "id": 120,
                    "word": val,
                    "pair": cur_word + " - " + val
                }
            # It requires a word ending in 's|ss + es'
            # Removes '-es' and look up in the set
            elif word_es and word_es[0][1] == 's' and word_es[0][0] in vocab.singular.only_ending_s:
                val = word_es[0][0]
                cur_data = {
                    "id": 130,
                    "word": val,
                    "pair": cur_word + " - " + val
                }
            # It requires a word ending in 'ch|sh|x|z + es'
            # Removes '-es' and look up in the set
            elif word_es and word_es[0][1] != 's' and word_es[0][0] in vocab.singular.singular_ending_non_s:
                val = word_es[0][0]
                cur_data = {
                    "id": 140,
                    "word": val,
                    "pair": cur_word + " - " + val
                }
            # It requires a word ending in 'ch|sh|x|z + es'
            # Removes '-es'
            elif word_es:
                val = word_es[0][0]
                cur_data = {
                    "id": 150,
                    "word": val,
                    "pair": cur_word + " - " + val
                }
            # Removes '-s'
            elif word_09:
                cur_data = {
                    "id": 160,
                    "word": cur_word,
                    "pair": ""
                }
            # Removes '-s'
            else:
                val = word_s[0]
                cur_data = {
                    "id": 170,
                    "word": val,
                    "pair": cur_word + " - " + val
                }

    # If data has changed
    if cur_data['id'] != cns.UNCHANGED_DATA_ID:
        # Log the word transformation pair
        logger.debug(f"(id={cur_data['id']}) {cur_word} -> {cur_data['word']}")
        # In case of design range violation
        if cur_data['id'] not in cur_range:
            raise exc.IdentifierOutOfRangeError(cur_data['id'], cur_range)

    return cur_data