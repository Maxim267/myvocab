import logging
from src.myvocab.utils.fetche_handler.fetcher import fetch

logger = logging.getLogger(__name__)

# Getting an IAM token for a Yandex account
# User must be registered in Yandex Cloud
# https://yandex.cloud/en/docs/iam/operations/iam-token/create


# Endpoint to exchange a code for a Yandex.OAuth token
URI_IAM_TOKENS = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'

headers = {}
data = {"yandexPassportOauthToken":"your_yandex_account"}

def fetch_iam_oauth() -> dict:
    """ Fetching an IAM token for a Yandex account.

    Returns:
        dict: JSON with the "iamToken" field
    """

    logger.info(f"Getting an IAM token for a Yandex account.")    
    return fetch(url=URI_IAM_TOKENS, headers=headers, payload=data)