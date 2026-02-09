import logging
import re
from pathlib import Path
from src.myvocab.constants import constants as cns
from src.myvocab.parsing.commands.save_file import save_file
from src.myvocab.translation.fetch_translate import fetch_translate

logger = logging.getLogger(__name__)

# Translation target chunk size (Yandex Translate API has a 10_000 character limit per request)
TRANSLATE_CHUNK_SIZE = 10_000
# Folder for sent and received translation chunks
TRANSLATE_FOLDER = 'Translate'

# Wrap a word in a template with an ID
def format_word(num: int, word: str) -> str:
    return '@' + str(num) + '@ ' + word + ' @'

def translate(iam: str, words: list, result_file_parent: Path, translated_words: dict = None, is_wrap_ids: bool = False) -> list:
    """
    Fetch translations for a list of words through an API.
    Args:
        iam: An IAM token is a unique sequence of characters issued to a user after authentication.
        words: The list of English words to be translated.
        result_file_parent: Target directory for the translation folder.
        translated_words: Caching translations for reuse.
        is_wrap_ids: Using an ID-tagged wrapper template to ensure reversible parsing: @d+@ word @.
    Returns:
        The List of bilingual word pairs.
    """

    # Create a new transformed list based on the existing one
    return_words = list(words)
    # Main index
    main_index = 0
    # Chunk number
    num_chunk = 0

    target_chunk_size = TRANSLATE_CHUNK_SIZE

    while main_index < len(words):
        start_index = main_index
        # Translation chunk list 
        chunk_list = list()
        # Mapping translation chunk IDs to the main list
        chunk_dict = dict()
        num_chunk += 1
        cur_size = 0
        # Chunk index
        chunk_index = 0
        for item in words[start_index:]:
            # If a translation attribute is found
            if find_list := re.findall(f'{cns.TAG_TRANSLATE}(.+)', item):
                # Get word to translate
                word = find_list[0]
                # Use cached translations
                if translated_words is not None and (translate_word := translated_words.get(word)):
                    return_words[main_index] = f"{word} - {translate_word}"
                    main_index += 1
                    continue
                # Use the template wrapper component
                elif is_wrap_ids:
                    non_format_word = word
                    word = format_word(chunk_index + 1, word)
                # Increase chunk size to a target size
                if cur_size + len(word) <= target_chunk_size:
                    chunk_index += 1
                    cur_size += len(word)
                    # Remove a translation attribute from a word in the returned list
                    if is_wrap_ids:
                        return_words[main_index] = non_format_word
                    else:
                        return_words[main_index] = word
                    # Append the word to the chunk list
                    chunk_list.append(word)
                    chunk_dict[chunk_index] = main_index
                else:
                    break
            main_index += 1

        # Translation chunk list is ready
        if len(chunk_list) > 0:
            logger.info(f"\n{num_chunk}: Translation ...")

            translate_path = Path.joinpath(result_file_parent, TRANSLATE_FOLDER)

            # Save outgoing chunk if log level is DEBUG
            if logger.getEffectiveLevel() == logging.DEBUG:
                if not translate_path.exists():
                    translate_path.mkdir(exist_ok=True, parents=True)
            if logger.getEffectiveLevel() == logging.DEBUG:
                save_file(Path.joinpath(translate_path, f"{num_chunk} chunk sent for translation.txt"), chunk_list, False)

            # Translate the chunk list
            fetch_data = fetch_translate(iam, chunk_list)

            # Save incoming chunk if log level is DEBUG
            if logger.getEffectiveLevel() == logging.DEBUG:
                Path(translate_path, f"{num_chunk} chunk received from the API.txt").write_text(data=f"{fetch_data}", encoding='utf-8')

            if fetch_data["ok"]:
                logger.info(f"{num_chunk}: Translation complete.")

                cnt = 0
                for text in fetch_data["translations"]:
                    for item in text.values():

                        # ID - based pattern parsing
                        if is_wrap_ids:
                            item = re.sub(r'(@\d+?@) *(.*?) *(@)', r'\1\2\3', item)
                            for word in re.findall(r'@(\d+?)@(.*?)@', item):
                                num = chunk_dict.get(int(word[0]))
                                if num is not None:
                                    # Cache the word
                                    if translated_words is not None:
                                        translated_words[return_words[num]] = word[1]
                                    # Bilingual word pair
                                    return_words[num] = return_words[num] + " - " + word[1]
                                    cnt += 1
                                    # The remaining data is logged to the error log
                                    chunk_dict.pop(int(word[0]))
                                else:
                                    logger.warning(f"Indeterminate word number: {int(word[0])}")
                                if cnt >= len(chunk_list):
                                    break
                        else:
                            # Parsing in original word order
                            cnt += 1
                            # Cache the word
                            if translated_words is not None:
                                translated_words[str(return_words[chunk_dict[cnt]])] = item
                            # Bilingual word pair
                            return_words[chunk_dict[cnt]] = str(return_words[chunk_dict[cnt]]) + " - " + item
                            if cnt >= len(chunk_list):
                                break

                if cnt == 0:
                    logger.warning(f"{num_chunk}: Data parsing ERROR. Unable to parse translation string.")
                elif cnt != len(chunk_list):
                    logger.warning(f"{num_chunk}: The number of transmitted and translated words does not match ({cnt - len(chunk_list)}).")
                    if is_wrap_ids:
                        logger.warning("Faulty word numbers: " + ",".join(f"{k}" for k in chunk_dict.keys()))
            else:
                logger.warning(f"{num_chunk}: Translation failed.")

    return return_words