import requests
import json
from tqdm import tqdm
from typing import List
import time
from datetime import datetime


CHEAT_STASH = {
    "id": "4baedf23834266c69db596b5cfa0bf35dbc7c92a3cf7c4fc634ac0b82f67b81e",
    "public": True,
    "accountName": "XiaZ",
    "stash": "~b/o 1 fuse",
    "stashType": "PremiumStash",
    "league": "Hardcore",
    "items": [
        {
            "verified": False,
            "w": 1,
            "h": 1,
            "icon": "https://web.poecdn.com/gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvSmV3ZWxzL01pZFF1ZXN0UmV3YXJkUmVkIiwidyI6MSwiaCI6MSwic2NhbGUiOjF9XQ/b920f106cf/MidQuestRewardRed.png",
            "league": "Hardcore",
            "id": "e768eb8f423f0ffc5cbf2e1e687f3e9f4289ff48565f2876b4a03033c3047c90",
            "name": "That Which Was Taken",
            "typeLine": "Crimson Jewel",
            "baseType": "Crimson Jewel",
            "rarity": "Unique",
            "ilvl": 1,
            "identified": True,
            "properties": [
                {"name": "Limited to", "values": [["1", 0]], "displayMode": 0}
            ],
            "explicitMods": [
                "8% increased Attack Damage",
                "+0.1 metres to Melee Strike Range",
            ],
            "descrText": "Place into an allocated Jewel Socket on the Passive Skill Tree. Right click to remove from the Socket.",
            "flavourText": ["A steady hand can hold back an army."],
            "frameType": 3,
            "extended": {"category": "jewels"},
            "x": 11,
            "y": 4,
            "inventoryId": "Stash11",
        }
    ],
}


class ItemDetector:
    wanted_items = {}
    found_items = {}

    def __init__(self) -> None:
        self.n_unique_items_found = 0

    def iterate_stashes(self, stashes: list) -> tuple:
        item_count = 0

        wanted_stashes = []
        leftover_stashes = []
        for stash in stashes:
            if stash["public"] and stash["items"]:
                stash_wanted_items = []
                stash_leftover_items = []
                for item in stash["items"]:
                    if self._check_item(item):
                        stash_wanted_items.append(item)
                        item_count += 1
                    else:
                        stash_leftover_items.append(item)

                stash["items"] = stash_leftover_items
                leftover_stashes.append(stash)
                if stash_wanted_items:
                    stash["items"] = stash_wanted_items
                    wanted_stashes.append(stash)

        self.n_unique_items_found = len(self.found_items.keys())
        return wanted_stashes, item_count, self.n_unique_items_found, leftover_stashes

    def _check_item(self, item: dict) -> bool:
        if item["baseType"] in self.wanted_items:
            if item["name"] in self.wanted_items[item["baseType"]]:
                self.found_items[item["name"] + " " + item["baseType"]] = True
                return True
        return False


class JewelDetector(ItemDetector):
    wanted_items = {
        "Cobalt Jewel": ["Grand Spectrum", "Forbidden Flesh"],
        "Crimson Jewel": ["That Which Was Taken", "Grand Spectrum", "Forbidden Flame"],
        "Viridian Jewel": ["Impossible Escape", "Grand Spectrum"],
        "Prismatic Jewel": ["Watcher's Eye", "Sublime Vision"],
        "Timeless Jewel": [
            "Glorius Vanity",
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
        self.url = url
        self.auth_token = auth_token
        self.headers["Authorization"] = "Bearer " + auth_token

        self.item_detectors = item_detectors

        self.n_found_items = 0
        self.n_wanted_items = n_wanted_items

        self.n_unique_items_found = 0
        self.n_unique_wanted_items = n_unique_wanted_items

    def _check_stashes(self, stashes):
        wanted_stashes = []
        n_new_items = 0
        n_total_unique_items = 0
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

        self.n_found_items += n_new_items
        self.item_count_pbar.update(n_new_items)

        self.unique_items_count_pbar.update(
            n_total_unique_items - self.n_unique_items_found
        )
        self.n_unique_items_found = n_total_unique_items

        return wanted_stashes

    def _initialize_stream(self) -> tuple:
        response = requests.get(self.url, headers=self.headers)
        response_json = response.json()

        stashes = response_json["stashes"]
        next_change_id = response_json["next_change_id"]

        # stashes.insert(0, CHEAT_STASH)
        stashes = self._check_stashes(stashes=stashes)

        self.iteration_pbar.update()
        return next_change_id, stashes

    def _get_up_stream(self, next_change_id: str) -> tuple:
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
        next_change_id = initial_next_change_id
        stashes = first_stashes
        new_stashes = ["FILLER"]

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
                    time.sleep(300)

                iteration += 1
        except requests.HTTPError as e:
            print(e)
        finally:
            self.iteration_pbar.close()
            self.item_count_pbar.close()
            self.unique_items_count_pbar.close()
            print(f"Final `next_change_id`: {next_change_id}")
            self._store_data(stashes=stashes)

    def dump_stream(
        self, initial_next_change_id: str = None, max_iterations: int = None
    ) -> None:
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
            if initial_next_change_id is None:
                next_change_id, stashes = self._initialize_stream()
            else:
                next_change_id = initial_next_change_id
                stashes = ["FILLER"]
            try:
                self._follow_stream(
                    initial_next_change_id=next_change_id,
                    first_stashes=stashes,
                    max_iterations=max_iterations,
                )
            except KeyboardInterrupt:
                print("Exiting program")

    def _store_data(self, stashes):
        print("Saving stashes")
        now = datetime.now().strftime("%Y_%m_%d %H_%m")
        with open(rf"testing_data\{now}.json", "w", encoding="utf-8") as infile:
            json.dump(stashes, infile, ensure_ascii=False, indent=4)


def main():
    auth_token = "***REMOVED***"
    url = "https://api.pathofexile.com/public-stash-tabs"

    n_wanted_items = 1000
    n_unique_wanted_items = 10

    api_handler = APIHandler(
        url=url,
        auth_token=auth_token,
        n_wanted_items=n_wanted_items,
        n_unique_wanted_items=n_unique_wanted_items,
    )
    api_handler.dump_stream(
        # initial_next_change_id="51782717-48721296-50468408-51725550-48651954"
    )  # max_iterations=100)

    return 0


if __name__ == "__main__":
    main()
