import logging

logger = logging.getLogger(__name__)

def handle_error(err) -> None:
    """ OS error handler. """

    cur_str = (
        f"{'-' * 40}"
        f"**ERROR handled in onerror function:**"
        f"Error accessing: {err.filename}"
        f"Error description: {err.strerror}"
        f"Error type: {type(err).__name__}"
        f"{'-' * 40}"
    )
    logger.warning(cur_str)