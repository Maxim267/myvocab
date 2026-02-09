import logging
from src.myvocab.utils.fetche_handler.fetcher import fetch

logger = logging.getLogger(__name__)

# Endpoint for translation
URI_TRANSLATE = 'https://translate.api.cloud.yandex.net/translate/v2/translate'

SOURCE_LANGUAGE_CODE = "en"
TARGET_LANGUAGE_CODE = "ru"
# Service account folder ID
FOLDER_ID = "b1gq1oofuk6esi44suvt"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer <KEY_IAM>",
}

payload = {
    "folderId": FOLDER_ID,
    "sourceLanguageCode": SOURCE_LANGUAGE_CODE,
    "targetLanguageCode": TARGET_LANGUAGE_CODE,
    "texts": list()
}

def fetch_translate(iam, words) -> dict:
    """ Fetching translations for the submitted word list. """

    headers["Authorization"] = f"Bearer {iam}"
    payload["texts"] = words
    return fetch(URI_TRANSLATE, headers=headers, payload=payload)