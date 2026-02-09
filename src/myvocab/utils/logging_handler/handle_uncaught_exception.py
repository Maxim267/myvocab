import logging
import traceback

logger = logging.getLogger(__name__)

def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    """ Log uncaught exceptions with a custom traceback. """

    tb = "".join(traceback.format_tb(exc_traceback))
    logger.critical(        
        f"\n{'='*40}\n"
        f"Uncaught exception: application will terminate.\n"
        f"Type: {exc_type.__name__}\n"
        f"Value: {exc_value}\n"
        f"Traceback:\n{tb}\n"
        f"{'='*40}"
    )

    input("Press Enter to exit...")