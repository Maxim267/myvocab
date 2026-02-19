import logging
from src.myvocab.utils.fetche_handler.fetcher import fetch
from src.myvocab.constants import constants as cns

logger = logging.getLogger(__name__)

# Getting an IAM token for a Yandex account
# User must be registered in Yandex Cloud
# https://yandex.cloud/en/docs/iam/operations/iam-token/create


data = {"yandexPassportOauthToken":"your_yandex_account"}

def fetch_iam_oauth() -> dict:
    """ Fetching an IAM token for a Yandex account.

    Returns:
        dict: JSON with the "iamToken" field
    """
    headers = {}

    logger.info(f"Getting an IAM token for a Yandex account.")    
    return fetch(url=cns.URI_IAM_TOKENS, headers=headers, payload=data)