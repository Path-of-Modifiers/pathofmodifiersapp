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
