from pathlib import Path
import re
from src.myvocab.exceptions import exceptions as exc

def get_file_unique_lines(file_path: Path) -> set:
    """ Get unique lines from a text file.

    Args:
        file_path (Path): File path
    Returns:
        set: Unique lines from a file
    """

    if not file_path.exists():
        raise exc.DirectoryNotExistError(file_path.resolve())
    if file_path.is_dir():
        raise exc.DirectoryIsNotFileError(file_path.resolve())   

    line_set = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        line_set = set(re.findall(r'(.+)\n*', content))

    return line_set