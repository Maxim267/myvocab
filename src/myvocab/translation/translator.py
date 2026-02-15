import logging
import re
from pathlib import Path
from src.myvocab.constants import constants as cns
from src.myvocab.exceptions import exceptions as exc
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

def translate(iam: str, words: list, result_directory: Path, translated_words: dict = None, is_wrap_ids: bool = False) -> list:
    """
    Fetch translations for a list of words through an API.
    Args:
        iam: An IAM token is a unique sequence of characters issued to a user after authentication.
        words: The list of English words to be translated.
        result_directory: Target directory for translation files.
        translated_words: Caching translations for reuse. If None, caching is skipped as input words are assumed to be unique.
        is_wrap_ids: Using an ID-tagged wrapper template to ensure reversible parsing: @d+@ word @.
    Returns:
        The List of bilingual word pairs.
    """

    # Populate a new list based on the input
    return_words = list(words)
    # Main index
    main_index = 0
    # Chunk number
    chunk_num = 0

    # Chunking for translation
    while main_index < len(words):
        start_index = main_index
        # Chunk of the word list
        chunk = list()
        # Extra chunk
        extra_chunk = list()
        # Chunk index
        chunk_index = 0

        # Map has two modes, depending on whether caching is used for translations:
        # 1: word -> list of all global indices of the word
        # 2: chunk index -> current global index of the word
        chunk_map = dict()

        chunk_num += 1
        # Chunk size
        chunk_size = 0
        # Template-wrapped word, activated by `is_wrap_ids`
        wrapped_word = ""

        for item in words[start_index:]:
            # If a translation attribute is found
            if find_list := re.findall(f'{cns.TAG_TRANSLATE}(.+)', item):
                # Get word to translate
                word = find_list[0]
                word_length = len(word)
                # Caching used words
                if translated_words is not None and (map_list := chunk_map.get(word)):
                    map_list.append(main_index)
                    return_words[main_index] = word
                    main_index += 1
                    continue
                # Caching translations
                elif translated_words is not None and (trns_word := translated_words.get(word)):
                    return_words[main_index] = f"{word} - {trns_word}"
                    main_index += 1
                    continue
                # Use the template wrapper component
                elif is_wrap_ids:
                    # Word wrapped in a template
                    wrapped_word = format_word(chunk_index + 1, word)
                    word_length = len(wrapped_word)
                # Increase chunk size to a target size
                if chunk_size + word_length <= TRANSLATE_CHUNK_SIZE:
                    chunk_size += word_length
                    chunk_index += 1

                    # Caching is used for translations
                    if translated_words is not None:
                        # 1: word -> list of all global indices of the word
                        cur_list = list()
                        cur_list.append(main_index)
                        chunk_map[word] = cur_list
                    else:
                        # 2: chunk index -> current global index of the word
                        chunk_map[chunk_index] = main_index

                    # Remove a translation attribute from a word in the returned list
                    return_words[main_index] = word

                    # Append the word to the chunk list
                    if is_wrap_ids:
                        chunk.append(wrapped_word)
                        extra_chunk.append(word)
                    else:
                        chunk.append(word)
                else:
                    # The chunk size is too small
                    if word_length > TRANSLATE_CHUNK_SIZE:
                        raise exc.ChunkSizeSmallError(TRANSLATE_CHUNK_SIZE, word_length)
                    break
            main_index += 1

        # Translation chunk list is ready
        if len(chunk) > 0:
            logger.info(f"\n{chunk_num}: Translation ...")

            translate_path = Path.joinpath(result_directory, TRANSLATE_FOLDER)

            # Save outgoing chunk if log level is DEBUG
            if logger.getEffectiveLevel() == logging.DEBUG:
                if not translate_path.exists():
                    translate_path.mkdir(exist_ok=True, parents=True)
            if logger.getEffectiveLevel() == logging.DEBUG:
                save_file(Path.joinpath(translate_path, f"{chunk_num} chunk sent for translation.txt"), chunk, False)

            # Translate the chunk list
            fetch_data = fetch_translate(iam, chunk)

            # Save incoming chunk if log level is DEBUG
            if logger.getEffectiveLevel() == logging.DEBUG:
                Path(translate_path, f"{chunk_num} chunk received from the API.txt").write_text(data=f"{fetch_data}", encoding='utf-8')

            if fetch_data["ok"]:
                logger.info(f"{chunk_num}: Translation complete.")

                cnt = 0
                for text in fetch_data["translations"]:
                    for item in text.values():

                        cnt += 1
                        if cnt > len(chunk):
                            logger.warning("Word count exceeded")
                            break

                        # ID - based pattern parsing
                        if is_wrap_ids:
                            item = re.sub(r'(@\d+?@) *(.*?) *(@)', r'\1\2\3', item)
                            for word in re.findall(r'@(\d+?)@(.*?)@', item):
                                ind = int(word[0])
                                if translated_words is not None:
                                    if ind not in range(1, len(chunk) + 1):
                                        logger.warning(f"Indeterminate word number: {ind}")
                                    else:
                                        eng_word = extra_chunk[ind - 1]
                                        translated_words[eng_word] = word[1]
                                else:
                                    num = chunk_map.get(ind)
                                    if num is not None:
                                        # Cache the word
                                        if translated_words is not None:
                                            translated_words[return_words[num]] = word[1]
                                        else:
                                            # Bilingual word pair
                                            return_words[num] = return_words[num] + " - " + word[1]
                                        # The remaining data is logged to the error log
                                        chunk_map.pop(ind)
                                    else:
                                        logger.warning(f"Indeterminate word number: {ind}")
                        else:
                            # Parsing in original word order
                            # Cache the word
                            if translated_words is not None:
                                translated_words[chunk[cnt - 1]] = item
                            else:
                                # Bilingual word pair
                                return_words[chunk_map[cnt]] = str(return_words[chunk_map[cnt]]) + " - " + item

                if cnt == 0:
                    logger.warning(f"{chunk_num}: Data parsing ERROR. Unable to parse translation string.")
                elif cnt != len(chunk):
                    logger.warning(f"{chunk_num}: The number of transmitted and translated words does not match ({cnt - len(chunk)}).")
                    if is_wrap_ids and translated_words is None:
                        logger.warning("Faulty word numbers: " + ",".join(f"{k}" for k in chunk_map.keys()))

                # Update return_words with translate
                if cnt > 0 and translated_words is not None:
                    for (key, cur_list) in chunk_map.items():
                        for ind in cur_list:
                            return_words[int(ind)] = str(return_words[int(ind)]) + " - " + translated_words[key]
            else:
                logger.warning(f"{chunk_num}: Translation failed.")

    return return_words