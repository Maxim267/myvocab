from pathlib import Path
import re
import os
from src.myvocab.exceptions import exceptions as exc

def validate_root_directory(root_path: Path):
    """ Validate root directory. """

    if root_path.is_file():
        raise exc.DirectoryIsNotFolderError(root_path.resolve())

    if not root_path.exists():
        raise exc.DirectoryNotExistError(root_path.resolve())

    if root_path.is_mount():
        raise exc.DirectoryIsMountError(root_path.resolve())

    if sys_dir := os.environ.get('SystemRoot'):
        if root_path.is_relative_to(sys_dir):
            raise exc.DirectoryIsSystemRootError(root_path.resolve())

def validate_file_name(reference_directory: Path, validate_filename: str):
    """ Validate filename. """

    cur_path = Path.joinpath(reference_directory, validate_filename)
    if reference_directory != cur_path.parent:
        raise exc.FileNameIsNotFileError(validate_filename)

def validate_bool_value(reference_bools: tuple, validate_bool: str):
    """ Validate a boolean value. """

    if validate_bool.lower() not in reference_bools:
        raise exc.NonBooleanValueError(validate_bool)

def validate_directory_with_leading_exclamation_mark(directory_path: Path | str, use_flag: bool, message: str = None):
    """ Validate that the directory path begins with "!". """

    if not use_flag:
        if isinstance(directory_path, Path):
            if re.findall(r'\\!|^!', str(directory_path.resolve())):
                if message is None:
                    raise exc.DirectoryExclamationMarkError(directory_path.resolve())
                else:
                    raise exc.DirectoryExclamationMarkError(directory_path.resolve(), message)
        elif re.findall(r'\\!|^!', directory_path):
            if message is None:
                raise exc.DirectoryExclamationMarkError(directory_path)
            else:
                raise exc.DirectoryExclamationMarkError(directory_path, message)