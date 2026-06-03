from pathlib import Path
from src.myvocab.parsing.commands.get_file_unique_lines import get_file_unique_lines

def diff_two_files(base_path: Path, compared_path: Path) -> list:
    """ Get the difference between two files.

    Args:
        base_path (Path): Base file path
        compared_path (Path): Compared file path
    Returns:
        list: Different lines
    """

    base_set = get_file_unique_lines(base_path)
    compared_set = get_file_unique_lines(compared_path)
    return_set = set()

    if base_set and not compared_set:
        return list(base_set)
    elif base_set and compared_set:
        for base_item in base_set:
            if base_item not in compared_set:
                # If the base_item is in base_file but not in compared_file
                return_set.add(base_item)

    return list(return_set)