import requests

def error_reason(response):
    print(response.status_code)
    print(response.reason)
    print(response.text)
    # print(response.json())
    quit()

def get_access_token(url, client_id, client_secret):
    """
    https://stackoverflow.com/questions/36719540/how-can-i-get-an-oauth2-access-token-using-python
    """
    url = "https://www.pathofexile.com/oauth/token"
    response = requests.post(
        url,
        data = {"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret, "scope": "service:psapi"},
        headers = {"Content-Type" : "application/x-www-form-urlencoded", "accept": "application/json", "User-Agent": "OAuth pathofmodifiers/0.1.0 (contact: ***REMOVED***) StrictMode"}
        # auth=(client_id, client_secret)
    )
    if response.status_code >= 300:
        error_reason(response)
    return response.json()["access_token"]

def main():
    url = "https://www.pathofexile.com/oauth/token"
    client_id = "pathofmodifiers"
    client_secret = "***REMOVED***"
    token = get_access_token(url, client_id, client_secret)
    print(token)
    # data = {"client_id":"pathofmodifers"}
    # response = requests.post("https://www.pathofexile.com/oauth/token")
    # if response.status_code >= 300:
    #     error_reason(response)

    return 0

if __name__ == "__main__":
    main()