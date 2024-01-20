import requests
import json
from tqdm import tqdm


class APIHandler:
    headers = headers = {
        "User-Agent": "OAuth pathofmodifiers/0.1.0 (contact: ***REMOVED***) StrictMode"
    }

    def __init__(self, url, auth_token):
        self.url = url
        self.auth_token = auth_token
        self.headers["Authorization"] = "Bearer " + auth_token

    def _initialize_stream(self, pbar):
        response = requests.get(self.url, headers=self.headers)
        response_json = response.json()

        stashes = response_json["stashes"]
        next_change_id = response_json["next_change_id"]
        # with open("testing.json", "w", encoding="utf-8") as infile:
        #     json.dump(stashes, infile, ensure_ascii=False, indent=4)

        pbar.update()
        return next_change_id, stashes

    def _get_up_stream(self, next_change_id):
        params = {"query": {"id": next_change_id}}

        response = requests.get(self.url, headers=self.headers, params=params)
        response_json = response.json()

        next_change_id = response_json["next_change_id"]
        stashes = response_json["stashes"]

        return next_change_id, stashes

    def _follow_stream(
        self, initial_next_change_id, first_stashes, max_iterations, pbar
    ):
        next_change_id = initial_next_change_id
        stashes = first_stashes

        iteration = 2
        try:
            while next_change_id and max_iterations >= iteration:
                next_change_id, new_stashes = self._get_up_stream(
                    next_change_id=next_change_id
                )
                stashes += ["NEW"] + new_stashes
                # with open("testing.json", "a", encoding="utf-8") as infile:
                #     json.dump(stashes, infile, ensure_ascii=False, indent=4)

                pbar.update()
                iteration += 1
        finally:
            pbar.close()
            print("Saving stashes")
            with open("testing.json", "w", encoding="utf-8") as infile:
                json.dump(stashes, infile, ensure_ascii=False, indent=4)

    def dump_stream(self, max_iterations: int = None):
        with tqdm(total=max_iterations) as pbar:
            next_change_id, stashes = self._initialize_stream(pbar=pbar)
            try:
                self._follow_stream(
                    initial_next_change_id=next_change_id,
                    first_stashes=stashes,
                    max_iterations=max_iterations,
                    pbar=pbar,
                )
            except KeyboardInterrupt:
                print("Exiting program")


def main():
    auth_token = "***REMOVED***"
    url = "https://api.pathofexile.com/public-stash-tabs"

    api_handler = APIHandler(url=url, auth_token=auth_token)
    api_handler.dump_stream(max_iterations=2)

    return 0


if __name__ == "__main__":
    main()
