import logging
import sys
import platform
from pathlib import Path
from dotenv import load_dotenv
from src.myvocab.utils.logging_handler.set_stream_handler import set_stream_handler
from src.myvocab.utils.logging_handler.handle_uncaught_exception import handle_uncaught_exception
from src.myvocab.utils.resource_handler.resource_path import resource_path
from src.myvocab.processing import processor as prc
from src.myvocab.utils.input_handler.input_yes_no import get_yes_no_input

# Root logger
logger = logging.getLogger(__name__)

def main(base_directory: Path, level: str):

    print(f"Python {platform.python_version()}")
    print(f"{sys.argv[0]}")

    sys.excepthook = handle_uncaught_exception
    set_stream_handler(level)

    dotenv_path = resource_path(Path('.env'))
    load_dotenv(dotenv_path=dotenv_path)

    if base_directory == "":
        base_directory = Path.cwd()
    print(f"The base directory for parsing text files: {str(base_directory.resolve())}")

    continue_program = get_yes_no_input("Do you want to continue?", default="yes")

    if continue_program:
        prc.render_vocab(base_directory)
        input("Press Enter to exit...")
    else:
        continue_program = get_yes_no_input("Do you want to enter a new directory for parsing text files?", default="yes")
        if continue_program:
            base_directory = Path(input("New base directory for parsing text files: "))
            prc.render_vocab(base_directory)
            input("Press Enter to exit...")

if __name__ == '__main__':

    index_d = None
    start_dir = ""
    for ind, arg in enumerate(sys.argv[1:]):
        if index_d is None and arg.lower() in ('-d', '-debug'):
            index_d = ind
            if index_d > 0:
                break
        else:
            if start_dir != "":
                start_dir += " "
            start_dir += arg

    cur_level = "" if index_d is None else "DEBUG"
    start_directory = Path(start_dir)
    main(start_directory, cur_level)