import logging
import re
from src.myvocab.parsing.vocabulary import vocabulary as vcb
from src.myvocab.exceptions import exceptions as exc
from src.myvocab.validators import validators as vld
from src.myvocab.constants import constants as cns
from src.myvocab.parsing.commands.write_settings import write_settings

logger = logging.getLogger(__name__)

def load_settings(vocab: vcb.VocabConfig) -> None:
    """ Load settings from a file.

    Update settings when the user modifies the settings file.

    Args:
        vocab (VocabConfig): 'Vocabulary configuration' object
    """

    if vocab.settings_file.is_dir():
        raise exc.DirectoryIsNotFileError(vocab.settings_file.resolve())

    if not vocab.settings_file.exists():
        write_settings(vocab)

    with open(vocab.settings_file, "r", encoding='utf-8') as file:
        content = file.read()
        for word in re.findall(r' *(.+?) *= *(.+) *', content):
            if word[0].strip() == 'result_file':
                try:
                    vld.validate_file_name(vocab.result_file.parent, word[1].strip())
                    vocab.result_file = word[1].strip()
                except exc.VocabError as e:
                    logger.warning(f"Invalid processing option '{word[0].strip()}': {e}")
            elif word[0].strip() == 'directories_file':
                try:
                    vld.validate_file_name(vocab.directories_file.parent, word[1].strip())
                    vocab.directories_file = word[1].strip()
                except exc.VocabError as e:
                    logger.warning(f"Invalid processing option '{word[0].strip()}': {e}")
            elif word[0].strip() == 'use_word_translate':
                try:
                    vld.validate_bool_value(cns.BOOLEAN_STRINGS, word[1].strip())
                    vocab.use_word_translate = (word[1].strip().lower() in cns.TRUTH_STRINGS)
                except exc.VocabError as e:
                    logger.warning(f"Invalid processing option '{word[0].strip()}': {e}")
            elif word[0].strip() == 'target_language_code':
                try:
                    target_language = vld.validate_target_language_code(word[1].strip(), vocab.target_languages_file)
                    vocab.target_language_code = target_language[0]
                    vocab.target_language = target_language[1]
                except exc.TargetLanguageCodeIsNotFoundError as e:
                    vocab.use_word_translate = False
                    logger.warning(f"Invalid processing option '{word[0].strip()}': {e}")
                except exc.VocabError as e:
                    logger.warning(f"Invalid processing option '{word[0].strip()}': {e}")
            elif word[0].strip() == 'use_lemma_singular':
                try:
                    vld.validate_bool_value(cns.BOOLEAN_STRINGS, word[1].strip())
                    vocab.use_lemma_singular = (word[1].strip().lower() in cns.TRUTH_STRINGS)
                except exc.VocabError as e:
                    logger.warning(f"Invalid processing option '{word[0].strip()}': {e}")
            elif word[0].strip() == 'use_lemma_infinit':
                try:
                    vld.validate_bool_value(cns.BOOLEAN_STRINGS, word[1].strip())
                    vocab.use_lemma_infinit = (word[1].strip().lower() in cns.TRUTH_STRINGS)
                except exc.VocabError as e:
                    logger.warning(f"Invalid processing option '{word[0].strip()}': {e}")
            elif word[0].strip() == 'use_order_text':
                try:
                    vld.validate_bool_value(cns.BOOLEAN_STRINGS, word[1].strip())
                    vocab.use_order_text = (word[1].strip().lower() in cns.TRUTH_STRINGS)
                except exc.VocabError as e:
                    logger.warning(f"Invalid processing option '{word[0].strip()}': {e}")
            elif word[0].strip() == 'use_folder_with_leading_exclamation_mark':
                try:
                    vld.validate_bool_value(cns.BOOLEAN_STRINGS, word[1].strip())
                    vocab.use_folder_with_leading_exclamation_mark = (word[1].strip().lower() in cns.TRUTH_STRINGS)
                    try:
                        message = "The base directory has the leading exclamation mark, but the 'use_folder_with_leading_exclamation_mark' option is set to false:"
                        vld.validate_directory_with_leading_exclamation_mark(vocab.base_directory.name, vocab.use_folder_with_leading_exclamation_mark, message)
                    except exc.VocabError as e:
                        logger.warning(f"Warning: {e}")
                except exc.VocabError as e:
                    logger.warning(f"Invalid processing option '{word[0].strip()}': {e}")