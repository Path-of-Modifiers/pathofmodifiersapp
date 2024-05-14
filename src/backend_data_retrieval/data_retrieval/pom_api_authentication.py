from requests.auth import HTTPBasicAuth
import os


FIRST_SUPERUSER = os.getenv("FIRST_SUPERUSER")
FIRST_SUPERUSER_PASSWORD = os.getenv("FIRST_SUPERUSER_PASSWORD")


def get_super_authentication() -> HTTPBasicAuth:
    authentication = HTTPBasicAuth(FIRST_SUPERUSER, FIRST_SUPERUSER_PASSWORD)
    return authentication
