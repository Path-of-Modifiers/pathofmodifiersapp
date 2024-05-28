from typing import Dict
from app.core.config import settings


def get_superuser_headers() -> Dict[str, str]:
    """Summary: Get the superuser headers for the API.

    Returns:
        dict[str, str]: The superuser headers.
    """
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    headers = {"Authorization": login_data}
    return headers
