import requests


def error_reason(response):
    print(response.status_code)
    print(response.reason)
    print(response.text)
    quit()


def get_access_token(url: str, client_id: str, client_secret: str) -> str:
    """
    https://stackoverflow.com/questions/36719540/how-can-i-get-an-oauth2-access-token-using-python
    """
    url = "https://www.pathofexile.com/oauth/token"
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
            "User-Agent": "OAuth pathofmodifiers/0.1.0 (contact: magnus.hoddevik@gmail.com) StrictMode",
        },
    )  # Sends necessary information required to generate a new OAuth2 Access Token
    if (
        response.status_code >= 300
    ):  # Prints relevant information in case of bad response
        error_reason(response)
    return response.json()["access_token"]


def main():
    url = "https://www.pathofexile.com/oauth/token"
    client_id = "pathofmodifiers"
    client_secret = "iF1xVCcdhFu9"  # Generated at: https://www.pathofexile.com/my-account/applications/pathofmodifiers/manage
    token = get_access_token(url=url, client_id=client_id, client_secret=client_secret)
    print(f"Generated a new token:\n {token}")
    return 0


if __name__ == "__main__":
    main()
