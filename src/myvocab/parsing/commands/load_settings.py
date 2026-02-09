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
                except Exception as e:
                    logger.warning(f"Invalid processing option '{word[0].strip()}': {e}")
            elif word[0].strip() == 'directories_file':
                try:
                    vld.validate_file_name(vocab.directories_file.parent, word[1].strip())
                    vocab.directories_file = word[1].strip()
                except Exception as e:
                    logger.warning(f"Invalid processing option '{word[0].strip()}': {e}")
            elif word[0].strip() == 'use_word_translate':
                try:
                    vld.validate_bool_value(cns.BOOLEAN_STRINGS, word[1].strip())
                    vocab.use_word_translate = (word[1].strip().lower() in cns.TRUTH_STRINGS)
                except Exception as e:
                    logger.warning(f"Invalid processing option '{word[0].strip()}': {e}")
            elif word[0].strip() == 'use_lemma_singular':
                try:
                    vld.validate_bool_value(cns.BOOLEAN_STRINGS, word[1].strip())
                    vocab.use_lemma_singular = (word[1].strip().lower() in cns.TRUTH_STRINGS)
                except Exception as e:
                    logger.warning(f"Invalid processing option '{word[0].strip()}': {e}")
            elif word[0].strip() == 'use_lemma_infinit':
                try:
                    vld.validate_bool_value(cns.BOOLEAN_STRINGS, word[1].strip())
                    vocab.use_lemma_infinit = (word[1].strip().lower() in cns.TRUTH_STRINGS)
                except Exception as e:
                    logger.warning(f"Invalid processing option '{word[0].strip()}': {e}")
            elif word[0].strip() == 'use_order_text':
                try:
                    vld.validate_bool_value(cns.BOOLEAN_STRINGS, word[1].strip())
                    vocab.use_order_text = (word[1].strip().lower() in cns.TRUTH_STRINGS)
                except Exception as e:
                    logger.warning(f"Invalid processing option '{word[0].strip()}': {e}")
            elif word[0].strip() == 'use_folder_with_leading_exclamation_mark':
                try:
                    vld.validate_bool_value(cns.BOOLEAN_STRINGS, word[1].strip())
                    vocab.use_folder_with_leading_exclamation_mark = (word[1].strip().lower() in cns.TRUTH_STRINGS)
                    try:
                        message = "The root directory has the leading exclamation mark, but the 'use_folder_with_leading_exclamation_mark' option is set to false:"
                        vld.validate_directory_with_leading_exclamation_mark(vocab.root_directory.name, vocab.use_folder_with_leading_exclamation_mark, message)
                    except Exception as e:
                        logger.warning(f"Warning: {e}")
                except Exception as e:
                    logger.warning(f"Invalid processing option '{word[0].strip()}': {e}")