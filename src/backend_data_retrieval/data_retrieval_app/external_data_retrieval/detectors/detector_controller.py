from typing import Any

import redis
from pydantic import TypeAdapter

from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.poe_schema import (
    CacheItem,
    CacheStash,
    Item,
    Stash,
)
from data_retrieval_app.external_data_retrieval.detectors.base import DetectorBase


class DetectorController:
    def __init__(
        self,
        detectors: list[DetectorBase],
        leagues: list[dict[str, Any]],
        redis_cache: redis.Redis,
    ):
        self.leagues = [league["name"] for league in leagues]

        self.detectors = detectors

        self.local_cache = dict[str, CacheStash]()
        self.local_cache[
            "158c93260022f9b39f9e7c6980711ab057c6ef2e28e1cdf00f2c2b5aef2c880c"
        ] = CacheStash(
            league="Standard",
            items=[
                CacheItem(  # changed price
                    id="1b6b82e172a31022acdc712dd59c641db1ce741352bdbcf967880e10f135e402_updated",
                    note="~b/o 2 mirror",
                ),
                CacheItem(  # same price
                    id="1b6b82e172a31022acdc712dd59c641db1ce741352bdbcf967880e10f135e402",
                    note="~b/o 30 chaos",
                ),
                CacheItem(  # removed
                    id="1b6b82e172a31022acdc712dd59c641db1ce741352bdbcf967880e10f135e402_removed",
                    note="~b/o 2 mirror",
                ),
            ],
        )
        self.cached_stash_adapter = TypeAdapter(list[CacheStash | None])
        self.redis_cache = redis_cache

    def _filter_duplicates(self, stashes: list[Stash]) -> list[Stash]:
        previous_ids = list[str]()
        non_duplicate_stashes = list[Stash]()
        for stash in stashes:
            if stash.id in previous_ids:
                continue

            previous_ids.append(stash.id)
            non_duplicate_stashes.append(stash)

        return non_duplicate_stashes

    def _filter_never_used(
        self, stashes: list[Stash]
    ) -> tuple[list[Stash], list[Stash]]:
        uninteresting_item_fields = {
            "monsterLevel",
            "lockedToCharacter",
            "lockedToAccount",
            "logbookMods",
            "ultimatumMods",
            "mercenarySkills",
            "isRelic",
            "enshrouded",
            "ruthless",
            "hybrid",
            "unmodifiableExceptChaos",
        }

        def has_price(note: str):
            return note is not None and note.startswith(("~b/o", "~price"))

        filtered_stashes = list[Stash]()
        empty_stashes = list[Stash]()
        for stash in stashes:
            items: list[Item] = stash.items
            filtered_items = []
            if not stash.public or stash.league not in self.leagues:
                # TODO should I already filter leagues? depends on what happens on migration
                print(stash.id)
                continue
            for item in items:
                if (
                    uninteresting_item_fields
                    & item.model_dump(exclude_none=True).keys()
                ):
                    continue

                if has_price(item.note):
                    pass
                elif has_price(stash.stash):
                    item.note = stash.stash
                else:
                    continue

                filtered_items.append(item)

            # print(len(filtered_items), stash.id)
            if filtered_items:
                stash.items = filtered_items
                filtered_stashes.append(stash)
            else:
                stash.items = []
                empty_stashes.append(stash)

        return filtered_stashes, empty_stashes

    def _filter_uninteresting_items(
        self, stashes: list[Stash]
    ) -> tuple[list[Stash], list[Item], list[Stash]]:
        interesting_stashes = list[Stash]()
        no_cache_new_items = list[Stash]()
        filtered_stashes = list[Stash]()
        for donor_stash in stashes:
            receiver_stash = donor_stash.model_copy(update={"items": []})
            no_cache_receiver_stash = donor_stash.model_copy(update={"items": []})
            for detector in self.detectors:
                # the donor stash is modified inplace, with its items moving over to the receiver stashes inplace
                detector.find_interesting_items(
                    donor_stash, receiver_stash, no_cache_receiver_stash
                )

            if receiver_stash.items:
                interesting_stashes.append(receiver_stash)
            elif no_cache_receiver_stash.items:
                # items such as unidentified items
                no_cache_new_items.extend(no_cache_receiver_stash.items)
            else:
                filtered_stashes.append(donor_stash)

        return interesting_stashes, no_cache_new_items, filtered_stashes

    def _get_cached_stashes(self, ids: list[str]) -> list[CacheStash | None]:
        """
        First checks local cache, then redis cache. This method relies on the local cache
        being exactly aligned with the redis cache for stashes that exists in both.
        """
        if len(ids) == 0:
            return []

        # first local cache
        cached_stashes = []
        still_needs_check = list[tuple[int, str]]()
        for i, id in enumerate(ids):
            cached_stash = self.local_cache.get(id)
            if cached_stash is None:
                still_needs_check.append((i, id))
            cached_stashes.append(cached_stash)

        # then redis cache
        redis_cached_stashes = self.cached_stash_adapter.validate_python(
            self.redis_cache.mget([id for _, id in still_needs_check])
        )
        for i, cached_stash in enumerate(redis_cached_stashes):
            if cached_stash is not None:
                idx, _ = still_needs_check[i]
                cached_stashes[idx] = cached_stash

        return cached_stashes

    def _find_removed_items(self, empty_stash_ids: list[str]) -> list[CacheItem]:
        # TODO what if league can change but id stays the same
        empty_cached_stashes = self._get_cached_stashes(empty_stash_ids)
        removed_items = list[CacheItem]()
        cached_stashes_to_remove = list[str]()
        for id, cached_stash in zip(empty_stash_ids, empty_cached_stashes, strict=True):
            if cached_stash is not None:
                print("cached stash must be removed", id)
                cached_stashes_to_remove.append(id)
                removed_items.extend(cached_stash.items)

        [self.local_cache.pop(id, None) for id in cached_stashes_to_remove]
        self.redis_cache.delete(cached_stashes_to_remove)

        return removed_items

    def _find_changed_items_filter_unchanged(
        self, stashes: list[Stash]
    ) -> tuple[list[Item], list[Item], list[CacheItem]]:
        # TODO what if league can change but id stays the same
        not_empty_stash_ids = [stash.id for stash in stashes]

        not_empty_cached_stashes = self._get_cached_stashes(not_empty_stash_ids)

        changed_items = list[Item]()
        new_items = list[Item]()
        removed_items = list[CacheItem]()

        stashes_to_cache = dict[str, CacheStash]()
        for cached_stash, stash in zip(not_empty_cached_stashes, stashes, strict=True):
            cached_stash_changed = False
            if cached_stash is not None:
                for cached_item in cached_stash.items[:]:
                    idx, new_item = stash.get_item(cached_item.id)
                    if new_item is None:
                        # a cached item doesnt exist anymore
                        print("cached item no longer exists", cached_item.id)
                        cached_stash_changed = True
                        cached_stash.items.remove(cached_item)
                        removed_items.append(cached_item)
                        continue
                    if new_item.note == cached_item.note:
                        # Duplicate found in cache
                        print("duplicate found", new_item.id)
                        stash.items.pop(idx)
                        continue

                    # Item has changed from cache
                    print("item has changed", new_item.id)
                    changed_items.append(new_item)
                    cached_stash_changed = True
                    cached_stash.items.remove(cached_item)

                cached_stash.items.extend(stash.to_cache().items)

            else:
                # The stash has never been cached
                cached_stash_changed = True
                cached_stash = stash.to_cache()

            new_items.extend(stash.items)

            if cached_stash_changed and cached_stash.items:
                stashes_to_cache[stash.id] = cached_stash

        self.local_cache.update(stashes_to_cache)
        self.redis_cache.mset(stashes_to_cache)

        return changed_items, new_items, removed_items

    def filter_stashes(
        self, stashes: list[Stash]
    ) -> tuple[list[CacheItem], list[Item], list[Item]]:
        """
        Returns:
            Removed items: items which need to be closed
            Changed items: items which need to start a new entry
            New items: items which need to be entered into the system
        """
        stashes = self._filter_duplicates(stashes)

        filtered_stashes, empty_stashes = self._filter_never_used(stashes)
        empty_stash_ids = [stash.id for stash in empty_stashes]

        (
            interesting_stashes,
            new_items,
            uninteresting_stashes,
        ) = self._filter_uninteresting_items(filtered_stashes)
        empty_stash_ids.extend([stash.id for stash in uninteresting_stashes])

        removed_items = self._find_removed_items(empty_stash_ids)

        (
            changed_items,
            more_new_items,
            more_removed_items,
        ) = self._find_changed_items_filter_unchanged(interesting_stashes)
        new_items.extend(more_new_items)
        removed_items.extend(more_removed_items)

        return removed_items, changed_items, new_items


if __name__ == "__main__":
    import json

    from data_retrieval_app.external_data_retrieval.detectors.unique_detector import (
        UniqueArmourDetector,
        UniqueJewelDetector,
        UniqueJewelleryDetector,
        UniqueUnidentifiedDetector,
        UniqueWeaponDetector,
    )

    class RedisCacheDecoy:
        cache = {
            "3ca7f08b3382795478397c41d110fc407da007bffd7e88dd9e6501bb306c7a6a": {
                # must be removed
                "league": "Standard",
                "items": [
                    {  # doesnt exist anymore
                        "id": "1b6b82e172a31022acdc712dd59c641db1ce741352bdbcf967880e10f135e402",
                        "note": "~b/o 30 chaos",
                    }
                ],
            },
            "eca1a8b071f18a3f07aa55f914173287a445f46b8e433ed3e04edf636dc6b946": {
                "league": "Allflame",
                "items": [
                    {  # duplicate
                        "id": "5588417cffcfbd0efe651cde0e5c606867d2b58a34812b90ce78e1352bacf68a",
                        "note": "~b/o 32 divine",
                    }
                ],
            },
        }

        def mget(self, keys: list[str]):
            return [self.cache.get(key) for key in keys]

        def mset(self, key_to_object: dict[str, Any]):
            for key, obj in key_to_object.items():
                self.cache[key] = obj

        def delete(self, keys: list[str]):
            for key in keys:
                self.cache.pop(key, None)

    detector_controller = DetectorController(
        [
            UniqueArmourDetector(),
            UniqueJewelDetector(),
            UniqueJewelleryDetector(),
            UniqueWeaponDetector(),
            UniqueUnidentifiedDetector(),
        ],
        [{"name": "Standard"}, {"name": "Hardcore"}, {"name": "Allflame"}],
        redis_cache=RedisCacheDecoy(),
    )

    stashes = json.load(open("stashes.json"))
    stashes = [
        stash
        for stash in stashes
        if stash["id"]
        in (
            "b3e32cdca2367d795b6d37b625bf22096ea2ee405b20357dc80c406dd0e4b63e",  # empty
            "ea0a95a395b48875e81f947cc87e315ba4a719fb08a5453f70c9e8c6fd2d0266",  # uninteresting
            "a68ead45e8bf786cec6c52d37a226739b5797f1c0264cf64321635f448dac97e",  # interesting
            "158c93260022f9b39f9e7c6980711ab057c6ef2e28e1cdf00f2c2b5aef2c880c",  # interesting
            "3ca7f08b3382795478397c41d110fc407da007bffd7e88dd9e6501bb306c7a6a",  # uninteresting
            "eca1a8b071f18a3f07aa55f914173287a445f46b8e433ed3e04edf636dc6b946",  # interesting
        )
    ]
    stash_adapter = TypeAdapter(list[Stash])
    stashes = stash_adapter.validate_python(stashes)
    detector_controller.filter_stashes(stashes)
