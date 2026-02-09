from re import findall
from pathlib import Path
from src.myvocab.parsing.vocabulary import vocabulary as vcb
from src.myvocab.validators import validators as vld
from src.myvocab.exceptions import exceptions as exc

def skip_current_dir(vocab: vcb.VocabConfig, current_dir_path: Path, partial_path: Path) -> bool:
   """ Check if the current directory should be ignored.

       Args:
        vocab (VocabConfig): 'Vocabulary configuration' object
        current_dir_path (Path): Current input directory
        partial_path (Path): Relative path starting from the parsing directory.
    Returns:
        bool: True to skip
   """

   try:
      # Ignore current directory prefixed with '!' if 'use_folder_with_leading_exclamation_mark' flag is unset
      vld.validate_directory_with_leading_exclamation_mark(partial_path, vocab.use_folder_with_leading_exclamation_mark)
   except exc.VocabError:
      return True

   # Exclude the resulting directory from parsing
   if (current_dir_path.is_relative_to(vocab.result_file.parent)
           or findall(rf'{vocab.result_file.parent.name}', str(partial_path))):
      return True

   return False