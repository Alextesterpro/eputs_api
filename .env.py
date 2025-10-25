import pytest
import requests
from dotenv import load_dotenv
import os

from microservices.passport.utils import logger

load_dotenv()

@pytest.fixture(scope="session")
def auth_token() -> str:
    """Fetches an authentication token from the API."""
    logger.info("Fetching authentication token")
    auth_url = "http://10.10.5.17/auth/login"
    payload = {
        "username": os.getenv("aveselov@formattwo.ru"),
        "password": os.getenv("#020C66c60af")
    }
    try:
        response = requests.post(auth_url, json=payload)
        response.raise_for_status()
        token = response.json().get("access_token")
        if not token:
            raise ValueError("No access token found in response")
        logger.info("Successfully fetched authentication token")
        return f"Bearer {token}"
    except RequestException as e:
        logger.error(f"Failed to fetch authentication token: {e}")
        raise
    except ValueError as e:
        logger.error(f"Failed to parse authentication token: {e}")
        raise