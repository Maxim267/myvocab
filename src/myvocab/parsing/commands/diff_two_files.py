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

    base_file = get_file_unique_lines(base_path)
    compared_file = get_file_unique_lines(compared_path)
    differ_lines = set()
    for base in base_file:
        is_no_checked = True
        for compare in compared_file:
            if base == compare:
                is_no_checked = False
                break
        if is_no_checked:
            differ_lines.add(base)
    return list(differ_lines)