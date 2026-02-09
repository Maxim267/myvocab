import logging
from pathlib import Path
import re
from src.myvocab.parsing.vocabulary import vocabulary as vcb
from src.myvocab.exceptions import exceptions as exc
from src.myvocab.validators import validators as vld
from src.myvocab.utils.walk_handler.handle_error import handle_error
from src.myvocab.parsing.commands.skip_current_dir import skip_current_dir

logger = logging.getLogger(__name__)

def write_directories(vocab: vcb.VocabConfig):
    """ Write the directory structure to a file.

    Save the directory structure to 'vocab.directories_file'.

    Args:
        vocab (VocabConfig): 'Vocabulary configuration' object
    """

    if vocab.directories_file.is_dir():
        raise exc.DirectoryIsNotFileError(vocab.settings_file.resolve())

    mark_folder = '📁'
    mark_file = '📄'

    old_lines = set()
    # old_dict = dict()
    new_lines = list()

    if vocab.directories_file.exists():  
        with open(vocab.directories_file, 'r', encoding = 'utf-8') as file:
            content = file.read()
            old_lines = re.findall(f'{mark_file} (.+txt) *(V+)', content)

    old_dict = dict(old_lines)
    offset = len(vocab.root_directory.parts) - 1

    # Path.walk traverses the directory tree, starting from the root
    for dirpath, dirs, files in Path.walk(vocab.root_directory, on_error = handle_error):

        dirpath_parts = Path(*dirpath.parts[offset::])

        # Check if the current directory should be ignored
        if skip_current_dir(vocab, dirpath, dirpath_parts):
            continue
            
        # Determine the nesting level
        level = len(dirpath.parts) - len(vocab.root_directory.parts)
        # Set the indentation to 4 spaces per level
        indent = ' ' * 4 * level

        # Show the current directory name
        # If the PyInstaller executable sets the root directory to '.'
        if level == 0 and dirpath.name == '':
            cur_list = re.split(r'[\\/]', str(vocab.root_directory.resolve()))
            new_lines.append(f'{indent}{mark_folder} {cur_list[len(cur_list) - 1]}/')
        else:
            new_lines.append(f'{indent}{mark_folder} {dirpath.name}/')
        
        # Increase the indentation level by 1 for all files in the current folder
        sub_indent = ' ' * 4 * (level + 1)

        # List the file names
        for file in files:

            # Text files only
            if not file.endswith(".txt"):
                continue
         
            try:
                # The current filename has the leading exclamation mark and the 'use_folder_with_leading_exclamation_mark' option is set to false
                cur_path = Path.joinpath(dirpath_parts, file)
                vld.validate_directory_with_leading_exclamation_mark(cur_path, vocab.use_folder_with_leading_exclamation_mark)
            except exc.VocabError:
                continue

            if old_dict.get(file):
                vend = ' ' + old_dict.get(file)
            else:
                vend = ''  
            new_lines.append(f'{sub_indent}{mark_file} {file}{vend}')

    if not vocab.directories_file.parent.exists():
        vocab.directories_file.parent.mkdir(exist_ok = True, parents = True)

    with open(vocab.directories_file, "w", encoding='utf-8') as file:
        file.writelines(f"{word}\n" for word in new_lines)

    logger.info(f"The directory tree is represented in: \n{vocab.directories_file.resolve()}\n")