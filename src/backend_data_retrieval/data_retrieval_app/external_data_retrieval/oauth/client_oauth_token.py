import requests

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.logs.logger import external_data_retrieval_logger as logger


def get_access_token(
    url: str, client_id: str, client_secret: str, contact_email: str
) -> str:
    """
    https://stackoverflow.com/questions/36719540/how-can-i-get-an-oauth2-access-token-using-python
    """
    url = "https://www.pathofexile.com/oauth/token"
    head_user_agent = (
        f"OAuth pathofmodifiers/0.1.0 (contact: {contact_email}) StrictMode"
    )
    response = requests.post(
        url,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "service:psapi",
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "accept": "application/json",
            "User-Agent": head_user_agent,
        },
    )  # Sends necessary information required to generate a new OAuth2 Access Token
    if (
        response.status_code >= 300
    ):  # Prints relevant information in case of bad response
        logger.exception(
            f"Error during get access token: {response.status_code} - {response.reason} - {response.text}"
        )
    return response.json()["access_token"]


def main():
    url = "https://www.pathofexile.com/oauth/token"
    client_id = settings.OAUTH_CLIENT_ID
    client_secret = settings.OAUTH_CLIENT_SECRET
    contact_email = settings.OATH_ACC_TOKEN_CONTACT_EMAIL
    token = get_access_token(
        url=url,
        client_id=client_id,
        client_secret=client_secret,
        contact_email=contact_email,
    )
    logger.info("Successfully generated token. Token is printed below")
    print("Token generated: " + token)
    return 0


if __name__ == "__main__":
    main()
