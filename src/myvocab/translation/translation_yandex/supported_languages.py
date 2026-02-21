import logging
import re
from pathlib import Path
from src.myvocab.utils.fetche_handler.fetcher import fetch
from src.myvocab.constants import constants as cns

logger = logging.getLogger(__name__)


def get_languages_list(fetch_langs: dict) -> list:
    """ Get the list of languages from the fetched supported languages. """
    langs = list()
    for item in fetch_langs["languages"]:
        langs.append(f"{item['code']}: {item['name']}")
    return  langs

def find_target_language_code(target_language_code: str, target_languages_file: Path) -> tuple:
    """ Find target language code in the supported languages file. """
    lang = ()
    if not target_languages_file.exists():
        return lang
    with open(file=target_languages_file, mode="r", encoding='utf-8') as f:
        content = f.read()
        if find_lang := re.findall(fr'({target_language_code}): *(.+)\n*', content):
            return find_lang[0]
    return lang

def fetch_languages(iam: str) -> dict:
    """ Fetching supported languages. """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {iam}"
    }

    payload = {
        "folderId": cns.FOLDER_ID
    }

    return fetch(cns.URI_LANGUAGES, headers=headers, payload=payload)