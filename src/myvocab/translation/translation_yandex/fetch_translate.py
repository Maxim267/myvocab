import logging
from src.myvocab.utils.fetche_handler.fetcher import fetch
from src.myvocab.constants import constants as cns

logger = logging.getLogger(__name__)


def fetch_translate(iam: str, words: list, target_language_code: str) -> dict:
    """ Fetching translations for the submitted word list. """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {iam}"
    }

    payload = {
        "folderId": cns.FOLDER_ID,
        "sourceLanguageCode": "en",
        "targetLanguageCode": f"{target_language_code}",
        "texts": words
    }

    return fetch(cns.URI_TRANSLATE, headers=headers, payload=payload)