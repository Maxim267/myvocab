import logging
import re
from pathlib import Path
from src.myvocab.utils.fetche_handler.fetcher import fetch
from src.myvocab.constants import constants as cns

logger = logging.getLogger(__name__)


def get_languages_list(fetch_langs: dict) -> list:
    langs = list()
    for item in fetch_langs["languages"]:
        langs.append(f"{item['code']}: {item['name']}")
    return  langs

def find_target_language_code(target_language_code: str, target_languages_file: Path) -> tuple:
    lang = ()
    if not target_languages_file.exists():
        return lang
    with open(file=target_languages_file, mode="r", encoding='utf-8') as f:
        content = f.read()
        if find_lang := re.findall(fr'({target_language_code}): *(.+)\n*', content):
            return find_lang[0]
    return lang

def fetch_languages(iam: str) -> dict:
    """ Fetching translations for the submitted word list. """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {iam}"
    }

    payload = {
        "folderId": cns.FOLDER_ID
    }

    return fetch(cns.URI_LANGUAGES, headers=headers, payload=payload)