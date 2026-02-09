import sys
from pathlib import Path

def resource_path(relative_path: Path) -> Path:
    """ Prepend the PyInstaller-generated folder to the PATH. """

    # PyInstaller creates a temp folder and stores path in _MEIPASS
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return Path.joinpath(Path(sys._MEIPASS), relative_path)
    else:
        return relative_path