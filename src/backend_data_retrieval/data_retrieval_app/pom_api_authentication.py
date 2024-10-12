import requests
from pydantic import HttpUrl

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.logs.logger import main_logger


def get_superuser_token_headers(url: HttpUrl) -> dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    try:
        r = requests.post(f"{url}/login/access-token", data=login_data)
        r.raise_for_status()
    except Exception as e:
        main_logger.exception(f"The following error occurred during the request: {e}")
        raise e
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
