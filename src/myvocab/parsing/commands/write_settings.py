import logging
from src.myvocab.parsing.vocabulary import vocabulary as vcb

logger = logging.getLogger(__name__)

def write_settings(vocab: vcb.VocabConfig) -> None:
    """ Write settings to a file.

    Save settings to 'vocab.settings_file'.

    Args:
        vocab (VocabConfig): 'Vocabulary configuration' object
    """

    if not vocab.settings_file.parent.exists():
        vocab.settings_file.parent.mkdir(exist_ok = True, parents = True)

    try:
        with open(vocab.settings_file, "w", encoding='utf-8') as file:
            cur_str = (
                f"result_file = {vocab.result_file.name}\n"
                f"directories_file = {vocab.directories_file.name}\n"
                f"use_lemma_singular = {vocab.use_lemma_singular}\n"
                f"use_lemma_infinit = {vocab.use_lemma_infinit}\n"
                f"use_word_translate = {vocab.use_word_translate}\n"
                f"target_language_code = {vocab.target_language_code}\n"
                f"use_order_text = {vocab.use_order_text}\n"
                f"use_folder_with_leading_exclamation_mark = {vocab.use_folder_with_leading_exclamation_mark}"
                )
            file.write(cur_str)
    except Exception as e:
        logger.exception(f"Failed to write file: {vocab.settings_file}: {type(e)} {e}")