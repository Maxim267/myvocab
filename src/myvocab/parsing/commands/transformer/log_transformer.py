import logging
from src.myvocab.constants import constants as cns

logger = logging.getLogger(__name__)


def log_transformer(payload: dict, changed: str) -> None:
    """ Log a specific transform. """
    # If data has changed
    if payload['id'] != cns.UNCHANGED_DATA_ID:
        # Log the word transformation pair
        logger.debug(f"(id={payload['id']}) {changed}")
