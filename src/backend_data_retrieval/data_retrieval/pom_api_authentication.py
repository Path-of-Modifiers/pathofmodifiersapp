from base64 import b64encode
from requests.auth import HTTPBasicAuth
import os


FIRST_SUPERUSER = os.getenv("FIRST_SUPERUSER")
FIRST_SUPERUSER_PASSWORD = os.getenv("FIRST_SUPERUSER_PASSWORD")


def get_super_authentication() -> HTTPBasicAuth:
    """
    Get the super authentication for the Path of Modifiers API.

    Returns:
        HTTPBasicAuth: POM user and password authentication.
    """
    authentication = HTTPBasicAuth(FIRST_SUPERUSER, FIRST_SUPERUSER_PASSWORD)
    return authentication


def get_basic_authentication() -> str:
    """
    Get the basic authentication for the Path of Modifiers API.

    Returns:
        str: Basic super user and super password authentication.
    """
    token = b64encode(
        f"{FIRST_SUPERUSER}:{FIRST_SUPERUSER_PASSWORD}".encode("utf-8")
    ).decode("ascii")
    return f"Basic {token}"
