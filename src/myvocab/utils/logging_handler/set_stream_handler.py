import logging
from logging import StreamHandler
import sys

logger = logging.getLogger(__name__)

def set_stream_handler(level: str) -> None:
    """ Set up custom logging configuration. """

    console_handler = StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    logging.basicConfig(
        encoding='utf-8',
        handlers=[console_handler],
        level = logging.DEBUG if level == 'DEBUG' else logging.INFO
   )
