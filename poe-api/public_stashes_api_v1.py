import requests
import pandas as pd
import json

def error_reason(response):
    print(response.status_code)
    print(response.reason)
    # print(response.json())

def main():
    auth_token = "***REMOVED***"
    headers = {"User-Agent": "OAuth pathofmodifiers/0.1.0 (contact: magnus.hoddevik@gmail.com) StrictMode", "Authorization": "Bearer " + auth_token}
    # stashes_filter = {"public": "true"}
    # params = {"stashes": json.dumps(stashes_filter)}
    # params = {"stashes": stashes_filter}
    params = {"query": {"stashes": {"public": "true"}}}
    # response = requests.get("https://api.pathofexile.com/public-stash-tabs", headers=headers, params=params)
    response = requests.get("https://api.pathofexile.com/public-stash-tabs", headers=headers, params=json.dumps(params))

    # response = requests.get("https://api.pathofexile.com/public-stash-tabs?stashes={'public':'true'}", headers=headers)
    print(response.url)
    if response.status_code >= 300:
        error_reason(response)
    
    with open("testing.json", "w", encoding="utf-8") as infile:
        json.dump(response.json(), infile, ensure_ascii=False, indent=4)

    
    return 0

if __name__ == "__main__":
    main()