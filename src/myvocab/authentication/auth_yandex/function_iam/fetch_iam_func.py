import logging
from src.myvocab.utils.fetche_handler.fetcher import get

logger = logging.getLogger(__name__)

# Using functions to get an IAM token for a service account
# https://yandex.cloud/ru/docs/functions/operations/function-sa


# Endpoint to invoke the public function
URI_IAM_TOKENS = 'https://functions.yandexcloud.net/d4ejta7dta3mi7jeti0n'

headers = {}

def fetch_iam_func() -> dict:
    """ Getting a Yandex service account IAM token via a public function. """

    logger.info(f"Using function to get an IAM token for a service account.")
    return get(url=URI_IAM_TOKENS, headers=headers)