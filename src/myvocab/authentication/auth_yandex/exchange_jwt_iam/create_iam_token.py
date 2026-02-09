import logging
import os
from pathlib import Path
import json
import yandexcloud
from yandex.cloud.iam.v1.iam_token_service_pb2 import (CreateIamTokenRequest)
from yandex.cloud.iam.v1.iam_token_service_pb2_grpc import IamTokenServiceStub
from src.myvocab.authentication.auth_yandex.exchange_jwt_iam.create_jwt import create_jwt
from src.myvocab.exceptions import exceptions as exc

logger = logging.getLogger(__name__)

# Get an IAM token using a JWT
# https://yandex.cloud/en/docs/iam/operations/iam-token/create-for-sa#python_2


def create_iam_token() -> str:
  """ Creating a Yandex IAM token from a service account JWT.

  Returns:
    str: IAM Token
  """

  logger.info(f"Get an IAM token using a JWT.")

  auth_key_path = os.getenv('AUTH_KEY_PATH')
  if not auth_key_path:
    raise exc.VariableIsNotFoundError('AUTH_KEY_PATH')

  key_path = Path(auth_key_path)

  # Reading a private key from a JSON file
  with open(file=key_path, mode='r', encoding='utf-8') as f:
    obj = f.read() 
    obj = json.loads(obj)
    private_key = obj['private_key']
    key_id = obj['id']
    service_account_id = obj['service_account_id']

  sa_key = {
    "id": key_id,
    "service_account_id": service_account_id,
    "private_key": private_key
  }

  jwt = create_jwt(key_path)
  
  sdk = yandexcloud.SDK(service_account_key=sa_key)
  iam_service = sdk.client(IamTokenServiceStub)
  iam = iam_service.Create(
      CreateIamTokenRequest(jwt=jwt)
  )

  return iam.iam_token