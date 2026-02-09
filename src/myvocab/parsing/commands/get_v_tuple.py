import logging
from pathlib import Path
import re
from src.myvocab.exceptions import exceptions as exc

logger = logging.getLogger(__name__)

def get_v_tuple(file_path: Path, v_number: int, delimiter: str = " ") -> dict:
    """ Get a map with 'V_Number' keys to 'V1' values.

    `file_path` is a delimited text file where each line has a fixed number of words.
    The position of each word determines its table column (V1, V2, etc.).
    Each file line number corresponds to its table row.
    Multiple values in one column are separated by a forward slash ('/').

    Args:
        file_path (Path): A tabular data file (like CSV).
        v_number (int): The table column number.
        delimiter (str, optional): The delimiter used to separate words. Defaults to " ".
    Returns:
        dict: Map with 'V_Number' keys to 'V1' values.
    """

    if not file_path.exists():
        raise exc.DirectoryNotExistError(file_path.resolve())
    if file_path.is_dir():
        raise exc.DirectoryIsNotFileError(file_path.resolve())  

    return_dict = dict()
    line_list = list()

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        line_list = re.findall(r'(.+)\n*', content)

    for index, line in enumerate(line_list):
        if len(delimiter) > 1:
            delimiter = delimiter.strip()
            if delimiter == "":
                delimiter = " "
        if delimiter == " ":
            split_tuple = re.split(r' +', line)
        else:
            split_tuple = re.split(fr' +{delimiter} +', line)

        if len(split_tuple) < v_number:
            try:
                raise exc.IndexOutOfRangeError(file_path)
            except Exception as e:
                logger.warning(f"Warning on line {index + 1} {split_tuple}: {e}")
                continue
        # V1
        v_1 = re.split(r'/', split_tuple[0].strip().lower())[0]
        # V_Number
        v_num = split_tuple[v_number - 1].strip().lower()
        # Multiple values in one column
        for item in re.split(r'/', v_num):
            if item != "":
                return_dict[item] = v_1

    return return_dict

def get_v1(file_path: Path, delimiter: str = " ") -> dict:
    """ Get a map with V1 keys and V1 values. """
    return get_v_tuple(file_path, 1, delimiter)

def get_v2(file_path: Path, delimiter: str = " ") -> dict:
    """ Get a map with V2 keys and V1 values. """
    return get_v_tuple(file_path, 2, delimiter)

def get_v3(file_path: Path, delimiter: str = " ") -> dict:
    """ Get a map with V3 keys and V1 values. """
    return get_v_tuple(file_path, 3, delimiter)
