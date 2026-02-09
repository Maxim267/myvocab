from pathlib import Path

def get_dir_size(dir_path: Path) -> int:
    """ Calculate the total size of a directory. """

    # Recursively sum the size of every file found
    return sum(f.stat().st_size for f in dir_path.rglob('*') if f.is_file())