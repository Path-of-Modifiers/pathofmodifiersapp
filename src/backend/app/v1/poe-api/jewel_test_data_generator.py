import requests
import json
from tqdm import tqdm
from typing import List
import time
from datetime import datetime


class ItemDetector:
    """
    Base class for searching stashes for items we want to store and process further
    """

    wanted_items = {}
    found_items = {}

    def __init__(self) -> None:
        """
        `self.n_unique_items_found` needs to be stored inbetween item detector sessions.
        """
        self.n_unique_items_found = 0

    def iterate_stashes(self, stashes: list) -> tuple:
        """
        Goes through all stashes searching for items that correspond to `self.wanted_items`.
        `self.n_unique_items_found` is calculated by the number of keys in `self.found_items`.
        The `_check_item` method, which is unique to item categories, is defined in a child class.

        Parameters:
            :param stashes: (list) A list of stash objects as defined by GGG.
            :return: (tuple) Wanted stashes, how many new items was found, number of different items that have been found so far, stashes that still need to be filtered.
        """
        item_count = 0

        # Lists of stashes to be populated
        wanted_stashes = []
        leftover_stashes = []
        for stash in stashes:
            if (
                stash["public"] and stash["items"]
            ):  # Checks if the stash is public and contains items
                # Lists of items
                stash_wanted_items = []
                stash_leftover_items = []
                for item in stash["items"]:
                    if self._check_item(item):  # Checks if we want the item
                        stash_wanted_items.append(item)
                        item_count += 1
                    else:
                        stash_leftover_items.append(item)

                # Replaces only the `items` object in stashes
                stash["items"] = stash_leftover_items
                leftover_stashes.append(stash)

                # Only adds stashes to `wanted_stashes` if items were found
                if stash_wanted_items:
                    stash["items"] = stash_wanted_items
                    wanted_stashes.append(stash)

        self.n_unique_items_found = len(self.found_items.keys())
        return wanted_stashes, item_count, self.n_unique_items_found, leftover_stashes


class UniqueDetector(ItemDetector):
    def _check_item(self, item: dict) -> bool:
        if (
            item["baseType"] in self.wanted_items
        ):  # Checks if the unique is a basetyp we are interested in
            if (
                item["name"] in self.wanted_items[item["baseType"]]
            ):  # Check if the unique is one that we want
                # Records the item as found, which is used to count number of unique items found
                self.found_items[item["name"] + " " + item["baseType"]] = True
                return True
        return False


class JewelDetector(UniqueDetector):
    """
    Contains only a dictionary of wanted uniques and with their basetype as
    """

    wanted_items = {
        "Cobalt Jewel": ["Grand Spectrum", "Forbidden Flesh"],
        "Crimson Jewel": ["That Which Was Taken", "Grand Spectrum", "Forbidden Flame"],
        "Viridian Jewel": ["Impossible Escape", "Grand Spectrum"],
        "Prismatic Jewel": ["Watcher's Eye", "Sublime Vision"],
        "Timeless Jewel": [
            "Glorious Vanity",
            "Lethal Pride",
            "Brutal Restraint",
            "Militant Faith",
            "Elegant Hubris",
        ],
        "Large Cluster Jewel": ["Voices"],
    }


class APIHandler:
    headers = {
        "User-Agent": "OAuth pathofmodifiers/0.1.0 (contact: magnus.hoddevik@gmail.com) StrictMode"
    }

    def __init__(
        self,
        url: str,
        auth_token: str,
        n_wanted_items: int = 100,
        n_unique_wanted_items: int = 5,
        item_detectors: list = [JewelDetector()],
    ) -> None:
        """
        Parameters:
            :param url: (str) A string containing POE public stash api url.
            :param auth_token: (str) A string containing OAuth2 auth token.
            :param n_wanted_items: (int) The number of items the program should search for before quitting.
            :param n_unique_wanted_items: (int) The number of different type of items the program should search for before quitin.
            :param item_detectors: (List[ItemDetector]) A list of `ItemDetector` instances.
        """
        self.url = url
        self.auth_token = auth_token
        self.headers["Authorization"] = "Bearer " + auth_token

        self.item_detectors = item_detectors

        self.n_found_items = 0
        self.n_wanted_items = n_wanted_items

        self.n_unique_items_found = 0
        self.n_unique_wanted_items = n_unique_wanted_items

    def _check_stashes(self, stashes: list) -> list:
        """
        Parameters:
            :param stashes: (list) A list of stash objects
        """
        wanted_stashes = []
        n_new_items = 0
        n_total_unique_items = 0

        # The stashes are fed to all item detectors, slowly being filtered down
        for item_detector in self.item_detectors:
            (
                filtered_stashes,
                item_count,
                n_unique_found_items,
                leftover_stashes,
            ) = item_detector.iterate_stashes(stashes)

            wanted_stashes += filtered_stashes
            n_new_items += item_count
            n_total_unique_items += n_unique_found_items

            stashes = leftover_stashes

        # Updates progress bars
        self.n_found_items += n_new_items
        self.item_count_pbar.update(n_new_items)

        self.unique_items_count_pbar.update(
            n_total_unique_items
            - self.n_unique_items_found  # Updates with the difference of current unique items found and previously found
        )
        self.n_unique_items_found = n_total_unique_items

        return wanted_stashes

    def _initialize_stream(self) -> tuple:
        """
        Used when no initial `next_change_id` is given
        """
        response = requests.get(self.url, headers=self.headers)
        response_json = response.json()

        stashes = response_json["stashes"]
        next_change_id = response_json["next_change_id"]

        stashes = self._check_stashes(stashes=stashes)

        self.iteration_pbar.update()
        return next_change_id, stashes

    def _get_up_stream(self, next_change_id: str) -> tuple:
        """
        Moves up in the stream and retrieves the new `stashes` and `next_change_id`

        Parameters:
            :param next_change_id: (str) An id generated by a previous API call
        """
        params = {"id": next_change_id}

        response = requests.get(self.url, headers=self.headers, params=params)

        if response.status_code >= 300:
            response.raise_for_status()

        response_json = response.json()

        next_change_id = response_json["next_change_id"]
        stashes = response_json["stashes"]

        return next_change_id, stashes

    def _follow_stream(
        self,
        initial_next_change_id: str,
        first_stashes: list,
        max_iterations: int,
    ) -> None:
        """
        Follows the API stream until conditions are met

        Parameters:
            :param initial_next_change_id: (str) A previously found `next_change_id`.
            :param first_stashes: (list) A list of stash objects which have already been found.
        """
        next_change_id = initial_next_change_id
        stashes = first_stashes
        new_stashes = []

        iteration = 2
        try:
            while (
                self.n_found_items < self.n_wanted_items
                or self.n_unique_items_found < self.n_unique_wanted_items
            ):
                next_change_id, new_stashes = self._get_up_stream(
                    next_change_id=next_change_id
                )
                wanted_stashes = self._check_stashes(stashes=new_stashes)
                stashes += wanted_stashes

                self.iteration_pbar.update()

                # if iteration >= max_iterations:
                #     break
                if not new_stashes:
                    time.sleep(
                        300
                    )  # Waits 5 minutes before continuing to persue the stream

                iteration += 1
        except requests.HTTPError as e:
            print(e)
        finally:  # Probably needs some more exception catches
            self.iteration_pbar.close()
            self.item_count_pbar.close()
            self.unique_items_count_pbar.close()
            print(f"Final `next_change_id`: {next_change_id}")
            self._store_data(stashes=stashes)

    def dump_stream(
        self, initial_next_change_id: str = None, max_iterations: int = None
    ) -> None:
        """
        The method which begins making API calls and fetching data.

        Parameters:
            :param initial_next_change_id: (str) A previously found `next_change_id`.
            :param max_iterations: (int) The number of iteration before shutting down. (currently not implemented)
        """

        # Intializes progressbar context managers
        with (
            tqdm(
                total=max_iterations, desc="Iterations", position=0
            ) as self.iteration_pbar,
            tqdm(
                total=self.n_wanted_items,
                desc="    Items found",
                unit="item",
                position=1,
            ) as self.item_count_pbar,
            tqdm(
                total=self.n_unique_wanted_items,
                desc="    Unique items found",
                unit="item",
                position=2,
            ) as self.unique_items_count_pbar,
        ):
            # Checks if an initial `next_change_id` was given
            if initial_next_change_id is None:
                next_change_id, stashes = self._initialize_stream()
            else:
                next_change_id = initial_next_change_id
                stashes = ["FILLER"]  # Random filler stash
            try:
                self._follow_stream(
                    initial_next_change_id=next_change_id,
                    first_stashes=stashes,
                    max_iterations=max_iterations,
                )
            except KeyboardInterrupt:
                print("Exiting program")

    def _store_data(self, stashes: list):
        """
        Stores the data as the program is done. All files are stored in the `.\testing_data` folder
        and named after the current time.
        """
        print("Saving stashes")
        now = datetime.now().strftime("%Y_%m_%d %H_%M")
        print(now)
        with open(rf"testing_data\{now}.json", "w", encoding="utf-8") as infile:
            json.dump(stashes, infile, ensure_ascii=False, indent=4)


def main():
    auth_token = "***REMOVED***"
    url = "https://api.pathofexile.com/public-stash-tabs"

    n_wanted_items = 10000
    n_unique_wanted_items = 15

    api_handler = APIHandler(
        url=url,
        auth_token=auth_token,
        n_wanted_items=n_wanted_items,
        n_unique_wanted_items=n_unique_wanted_items,
    )
    api_handler.dump_stream(
        initial_next_change_id="2304265269-2292493816-2218568823-2460180973-2390424272"  # From poe.ninja
    )  # max_iterations=100)

    return 0


if __name__ == "__main__":
    main()
