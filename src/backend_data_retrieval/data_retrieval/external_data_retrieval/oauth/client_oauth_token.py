import requests
import os


OATH_ACC_TOKEN_CONTACT_EMAIL = os.getenv("OATH_ACC_TOKEN_CONTACT_EMAIL")
OAUTH_CLIENT_ID = os.getenv("OAUTH_CLIENT_ID")
OAUTH_CLIENT_SECRET = os.getenv("OAUTH_CLIENT_SECRET")

def error_reason(response):
    print(response.status_code)
    print(response.reason)
    print(response.text)
    quit()


def get_access_token(url: str, client_id: str, client_secret: str, contact_email: str) -> str:
    """
    https://stackoverflow.com/questions/36719540/how-can-i-get-an-oauth2-access-token-using-python
    """
    url = "https://www.pathofexile.com/oauth/token"
    head_user_agent = f"OAuth pathofmodifiers/0.1.0 (contact: {contact_email}) StrictMode"
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
            f"User-Agent": head_user_agent,
        },
    )  # Sends necessary information required to generate a new OAuth2 Access Token
    if (
        response.status_code >= 300
    ):  # Prints relevant information in case of bad response
        error_reason(response)
    return response.json()["access_token"]


def main():
    url = "https://www.pathofexile.com/oauth/token"
    client_id = OAUTH_CLIENT_ID
    client_secret = OAUTH_CLIENT_SECRET  # Generated at: https://www.pathofexile.com/my-account/applications/pathofmodifiers/manage
    token = get_access_token(url=url, client_id=client_id, client_secret=client_secret)
    print(f"Generated a new token:\n {token}")
    return 0


if __name__ == "__main__":
    main()
