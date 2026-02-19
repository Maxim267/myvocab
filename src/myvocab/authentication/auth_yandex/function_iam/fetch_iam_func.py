import logging
from src.myvocab.utils.fetche_handler.fetcher import get
from src.myvocab.constants import constants as cns

logger = logging.getLogger(__name__)

# Using functions to get an IAM token for a service account
# https://yandex.cloud/ru/docs/functions/operations/function-sa


def fetch_iam_func() -> dict:
    """ Getting a Yandex service account IAM token via a public function. """

    headers = {}

    logger.info(f"Using function to get an IAM token for a service account.")
    return get(url=cns.URI_FUNC_IAM_TOKENS, headers=headers)