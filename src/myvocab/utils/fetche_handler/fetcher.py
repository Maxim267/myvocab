import requests
import logging

logger = logging.getLogger(__name__)

def fetch(url: str, headers: dict, payload: dict) -> dict:
    """ Fetch data from the given URL using the provided headers and payload. """

    data = {}
    try:
        # 1. Send the POST request with a timeout (crucial for error handling)
        response = requests.post(url=url, json=payload, headers=headers, timeout=10)

        # 1.1. Process the successful response
        data = response.json()

        data["ok"] = response.ok
        data["status_code"] = response.status_code
        data["reason"] = response.reason

        # 2. Raise an exception if the server returns an error code (4xx or 5xx)
        response.raise_for_status()

    except requests.exceptions.HTTPError as http_err:
        logger.warning(f"HTTP error occurred: {http_err}\n{data['message']}")  # e.g., 404 Not Found or 500 Server Error
    except requests.exceptions.ConnectionError:
        logger.warning("Connection error: Check your internet or the server URL.")
    except requests.exceptions.Timeout:
        logger.warning("The request timed out.")
    except requests.exceptions.RequestException as err:
        logger.warning(f"An unexpected error occurred: {err}")

    return data

def get(url: str, headers: dict) -> dict:
    """ Get data from the given URL using the provided headers. """

    data = {}
    try:
        # 1. Send the GET request with a timeout (crucial for error handling)
        response = requests.get(url=url, headers=headers, timeout=10)

        # 1.1. Process the successful response
        data = response.json()

        data["ok"] = response.ok
        data["status_code"] = response.status_code
        data["reason"] = response.reason

        # 2. Raise an exception if the server returns an error code (4xx or 5xx)
        response.raise_for_status()

    except requests.exceptions.HTTPError as http_err:
        logger.warning(f"HTTP error occurred: {http_err}\n{data['message']}")  # e.g., 404 Not Found or 500 Server Error
    except requests.exceptions.ConnectionError:
        logger.warning("Connection error: Check your internet or the server URL.")
    except requests.exceptions.Timeout:
        logger.warning("The request timed out.")
    except requests.exceptions.RequestException as err:
        logger.warning(f"An unexpected error occurred: {err}")

    return data