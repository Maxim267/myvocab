import logging
from pathlib import Path
import time
import jwt
import json
from src.myvocab.constants import constants as cns

logger = logging.getLogger(__name__)

# Get an IAM token using a JWT
# https://yandex.cloud/en/docs/iam/operations/iam-token/create-for-sa#python_2


def create_jwt(key_path: Path) -> str:
    """ Creating a JWT for a Yandex service account.

    Args:
        key_path (Path): Path to the Yandex service account key JSON file
    Returns:
        str: JSON Web Token
    """

    logger.info(f"Generating a JWT .")

    # Reading a private key from a JSON file
    with open(file=key_path, mode='r', encoding='utf-8') as f:
        obj = f.read() 
        obj = json.loads(obj)
        private_key = obj['private_key']
        key_id = obj['id']
        service_account_id = obj['service_account_id']

    now = int(time.time())
    payload = {
            'aud': cns.URI_IAM_TOKENS,
            'iss': service_account_id,
            'iat': now,
            'exp': now + 3600
        }

    # JWT generation.
    encoded_token = jwt.encode(
        payload,
        private_key,
        algorithm='PS256',
        headers={'kid': key_id}
    )

    return encoded_token