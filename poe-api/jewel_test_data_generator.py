import requests
import json
from tqdm import tqdm
from typing import List


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

    def __init__(self) -> None:
        pass

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

        return wanted_stashes, item_count, leftover_stashes

    def _check_item(self, item: dict) -> bool:
        if item["baseType"] in self.wanted_items:
            if item["name"] in self.wanted_items[item["baseType"]]:
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
    headers = headers = {
        "User-Agent": "OAuth pathofmodifiers/0.1.0 (contact: magnus.hoddevik@gmail.com) StrictMode"
    }

    def __init__(
        self,
        url: str,
        auth_token: str,
        n_wanted_items: int = 100,
        item_detectors: list = [JewelDetector()],
    ) -> None:
        self.url = url
        self.auth_token = auth_token
        self.headers["Authorization"] = "Bearer " + auth_token

        self.item_detectors = item_detectors

        self.n_found_items = 0
        self.n_wanted_items = n_wanted_items

    def _check_stashes(self, stashes):
        wanted_stashes = []
        n_new_items = 0
        for item_detector in self.item_detectors:
            (
                filtered_stashes,
                item_count,
                leftover_stashes,
            ) = item_detector.iterate_stashes(stashes)

            wanted_stashes += filtered_stashes
            n_new_items += item_count

            stashes = leftover_stashes

        self.n_found_items += n_new_items

        return wanted_stashes

    def _initialize_stream(self, pbar) -> tuple:
        response = requests.get(self.url, headers=self.headers)
        response_json = response.json()

        stashes = response_json["stashes"]
        next_change_id = response_json["next_change_id"]

        # stashes.insert(0, CHEAT_STASH)
        stashes = self._check_stashes(stashes=stashes)

        pbar.update()
        return next_change_id, stashes

    def _get_up_stream(self, next_change_id: str) -> tuple:
        params = {"id": next_change_id}

        response = requests.get(self.url, headers=self.headers, params=params)
        response_json = response.json()

        next_change_id = response_json["next_change_id"]
        stashes = response_json["stashes"]

        return next_change_id, stashes

    def _follow_stream(
        self,
        initial_next_change_id: str,
        first_stashes: list,
        max_iterations: int,
        pbar,
    ) -> None:
        next_change_id = initial_next_change_id
        stashes = first_stashes
        new_stashes = ["FILLER"]

        iteration = 2
        try:
            while new_stashes and self.n_found_items < self.n_wanted_items:
                next_change_id, new_stashes = self._get_up_stream(
                    next_change_id=next_change_id
                )
                wanted_stashes = self._check_stashes(stashes=new_stashes)
                stashes += wanted_stashes

                pbar.update()

                # if iteration >= max_iterations:
                #     break
                iteration += 1
        except KeyError as e:
            print(e)
        finally:
            pbar.close()
            print("Saving stashes")
            with open("testing.json", "w", encoding="utf-8") as infile:
                json.dump(stashes, infile, ensure_ascii=False, indent=4)

    def dump_stream(self, max_iterations: int = None) -> None:
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
    auth_token = "750d4f685cfa83d024d86508e7ede4ab55b5acc7"
    url = "https://api.pathofexile.com/public-stash-tabs"

    api_handler = APIHandler(url=url, auth_token=auth_token)
    api_handler.dump_stream()  # max_iterations=100)

    return 0


if __name__ == "__main__":
    main()
