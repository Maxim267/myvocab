import logging
from pathlib import Path
import re
import os
from src.myvocab.exceptions import exceptions as exc
from src.myvocab.authentication.auth_yandex.function_iam.fetch_iam_func import fetch_iam_func
from src.myvocab.translation.translation_yandex.supported_languages import fetch_languages
from src.myvocab.translation.translation_yandex.supported_languages import get_languages_list
from src.myvocab.translation.translation_yandex.supported_languages import find_target_language_code
from src.myvocab.parsing.commands.save_file import save_file

logger = logging.getLogger(__name__)

def validate_base_directory(base_path: Path) -> None:
    """ Validate base directory. """

    if base_path.is_file():
        raise exc.DirectoryIsNotFolderError(base_path.resolve())

    if not base_path.exists():
        raise exc.DirectoryNotExistError(base_path.resolve())

    if base_path.is_mount():
        raise exc.DirectoryIsMountError(base_path.resolve())

    if sys_dir := os.environ.get('SystemRoot'):
        if base_path.is_relative_to(sys_dir):
            raise exc.DirectoryIsSystemRootError(base_path.resolve())

def validate_file_name(reference_directory: Path, validate_filename: str) -> None:
    """ Validate filename. """

    cur_path = Path.joinpath(reference_directory, validate_filename)
    if reference_directory != cur_path.parent:
        raise exc.FileNameIsNotFileError(validate_filename)

def validate_bool_value(reference_bools: tuple, validate_bool: str) -> None:
    """ Validate a boolean value. """

    if validate_bool.lower() not in reference_bools:
        raise exc.NonBooleanValueError(validate_bool)

def validate_directory_with_leading_exclamation_mark(directory_path: Path | str, use_flag: bool, message: str = None) -> None:
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

def validate_target_language_code(target_language_code: str, target_languages_file: Path) -> tuple:
    """ Validate the target language.

    Args:
        target_language_code (str): Target language code
        target_languages_file (Path): Target languages file
    Returns:
        tuple: Target language code and name.
    """

    def create_target_languages_file(trg_languages_file: Path) -> None:
        """ Create the target language file. """
        fetch_data = fetch_iam_func()
        if iam_token := fetch_data.get("access_token"):
            fetch_langs = fetch_languages(iam_token)
            if not fetch_langs["ok"]:
                raise exc.FetchSupportedLanguagesError("")
            langs = get_languages_list(fetch_langs)
            save_file(file_path=trg_languages_file, items=langs, is_sorted=False)
        else:
            raise exc.FetchIAMtokenError("during target language validation.")
    # Find the target language code
    target_language = find_target_language_code(target_language_code, target_languages_file)
    if not target_language:
        create_target_languages_file(target_languages_file)
        target_language = find_target_language_code(target_language_code, target_languages_file)
        if target_language:
            return target_language
        else:
            raise exc.TargetLanguageCodeIsNotFoundError(target_language_code)
    else:
        return target_language