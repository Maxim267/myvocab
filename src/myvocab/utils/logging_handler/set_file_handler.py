import logging
from pathlib import Path
from src.myvocab.exceptions import exceptions as exc

def set_file_handler(log_file_path: Path):
    """ Add the custom FileHandler to the root logger. """

    if log_file_path.is_dir():
        raise exc.DirectoryIsNotFileError(log_file_path.resolve()) 
    if not log_file_path.parent.exists():
        log_file_path.parent.mkdir(exist_ok=True, parents=True)

    # Get the root logger
    root_logger = logging.getLogger()

    # Remove existing FileHandlers from the root logger
    for handler in root_logger.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            root_logger.removeHandler(handler)
            handler.close()

    # Create a new FileHandler
    new_file_handler = logging.FileHandler(str(log_file_path.resolve()), mode='w', encoding='utf-8')
    new_file_handler.setLevel(logging.DEBUG)

    # Define a formatter and apply it to the new handler
    formatter = logging.Formatter(fmt='[%(asctime)s] %(levelname)s - %(name)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    new_file_handler.setFormatter(formatter)

    # Add the new FileHandler to the root logger
    root_logger.addHandler(new_file_handler)

    # Log a message to confirm the change
    root_logger.info(f"Logging to file changed to: \n{str(log_file_path.resolve())}\n")