from typing import Any

import redis
from backend_api.app.core.schemas.league import League
from pydantic import TypeAdapter

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.external.poe import (
    PoeItem,
    Stash,
)
from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.internal.cache import (
    CacheItem,
    CacheItemWithContext,
    CacheStash,
)
from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.internal.categorized import (
    OrganizedItems,
    OrganizedItemsByCategory,
)
from data_retrieval_app.external_data_retrieval.detectors.base import (
    CategoryDetectorBase,
)
from data_retrieval_app.external_data_retrieval.utils import (
    sync_timing_tracker,
)
from data_retrieval_app.logs.logger import data_retrieval_logger as logger


class DetectorController:
    backend_base_url = settings.BACKEND_BASE_URL
    existing_items_url = f"{backend_base_url}/item/existing/"

    def __init__(
        self,
        detectors: list[CategoryDetectorBase],
        leagues: list[League],
    ):
        self.leagues = [league.name for league in leagues]

        self.detectors = detectors

        self.local_cache = dict[str, CacheStash]()
        self.cached_stash_adapter = TypeAdapter(list[CacheStash | None])

    def _filter_duplicates(self, stashes: list[Stash]) -> list[Stash]:
        previous_ids = list[str]()
        non_duplicate_stashes = list[Stash]()
        duplicates_found = 0
        for stash in reversed(stashes):
            if stash.id in previous_ids:
                duplicates_found += 1
                continue

            previous_ids.append(stash.id)
            non_duplicate_stashes.append(stash)

        logger.info(f"Filtered away {duplicates_found} duplicate stashes")
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

        filtered_stashes = list[Stash]()
        empty_stashes = list[Stash]()

        n_uninteresting_items = 0
        n_items_in = 0

        for stash in stashes:
            items: list[PoeItem] = stash.items
            filtered_items = []
            if not stash.public or stash.league not in self.leagues:
                # TODO should I already filter leagues? depends on what happens on migration
                continue
            n_items_in += len(items)
            for item in items:
                if (
                    uninteresting_item_fields
                    & item.model_dump(exclude_none=True).keys()
                ):
                    # if any of these fields are present, it automatically means we are not interested
                    n_uninteresting_items += 1
                    continue

                if item.has_price():
                    pass
                elif stash.has_price():
                    item.note = stash.stash
                else:
                    n_uninteresting_items += 1
                    continue

                filtered_items.append(item)

            if filtered_items:
                stash.items = filtered_items
                filtered_stashes.append(stash)
            else:
                stash.items = []
                empty_stashes.append(stash)

        logger.info(
            f"task=filter_never_used n_stashes_in={len(stashes)} n_stashes_found={len(filtered_stashes)} n_items_in={n_items_in} n_items_filtered={n_uninteresting_items}"
        )
        return filtered_stashes, empty_stashes

    def _filter_uninteresting_items(
        self, stashes: list[Stash]
    ) -> tuple[list[Stash], list[PoeItem], list[Stash]]:
        n_uninteresting_items = 0
        n_items_in = 0

        interesting_stashes = list[Stash]()
        no_cache_new_items = list[PoeItem]()
        filtered_stashes = list[Stash]()
        for donor_stash in stashes:
            n_items_in += len(donor_stash.items)
            receiver_stash = donor_stash.model_copy(update={"items": []})
            no_cache_receiver_stash = donor_stash.model_copy(update={"items": []})
            for detector in self.detectors:
                # the donor stash is modified inplace, with its items moving over to the receiver stashes inplace
                detector.find_interesting_items(
                    donor_stash, receiver_stash, no_cache_receiver_stash
                )

            if receiver_stash.items:
                interesting_stashes.append(receiver_stash)

            if no_cache_receiver_stash.items:
                # items such as unidentified items
                no_cache_new_items.extend(no_cache_receiver_stash.items)

            n_uninteresting_items += len(donor_stash.items)

            filtered_stashes.append(donor_stash)

        logger.info(
            f"task=filter_uninteresting n_stashes_in={len(stashes)} n_stashes_filtered={len(filtered_stashes)} n_items_in={n_items_in} n_items_filtered={n_uninteresting_items}"
        )
        return interesting_stashes, no_cache_new_items, filtered_stashes

    def _get_cached_stashes(
        self, redis_cache: redis.Redis, ids: list[str]
    ) -> list[CacheStash | None]:
        """
        First checks local cache, then redis cache. This method relies on the local cache
        being exactly aligned with the redis cache for stashes that exists in both.
        """
        if len(ids) == 0:
            return []

        # first local cache
        cached_stashes = list[CacheStash | None]()
        still_needs_check = list[tuple[int, str]]()
        for i, id in enumerate(ids):
            cached_stash = self.local_cache.get(f"stash:{id}")
            if cached_stash is None:
                still_needs_check.append((i, id))
            cached_stashes.append(cached_stash)

        # then redis cache
        redis_cached_stashes = self.cached_stash_adapter.validate_python(
            redis_cache.mget([f"stash:{id}" for _, id in still_needs_check])
        )
        for i, cached_stash in enumerate(redis_cached_stashes):
            if cached_stash is not None:
                idx, _ = still_needs_check[i]
                cached_stashes[idx] = cached_stash

        return cached_stashes

    def _find_removed_items(
        self, empty_stash_ids: list[str], redis_cache: redis.Redis
    ) -> list[CacheItem]:
        # TODO what if league can change but id stays the same
        empty_cached_stashes = self._get_cached_stashes(redis_cache, empty_stash_ids)
        removed_items = list[CacheItem]()
        cached_stashes_to_remove = list[str]()

        for id, cached_stash in zip(empty_stash_ids, empty_cached_stashes, strict=True):
            if cached_stash is not None:
                cached_stashes_to_remove.append(f"stash:{id}")
                removed_items.extend(cached_stash.items)

        if cached_stashes_to_remove:
            [self.local_cache.pop(id, None) for id in cached_stashes_to_remove]
            redis_cache.delete(*cached_stashes_to_remove)

        logger.info(
            f"task=find_removed n_stashes_in={len(empty_stash_ids)} n_stashes_cached={len(cached_stashes_to_remove)} n_removed_items={len(removed_items)}"
        )
        return removed_items

    def _find_changed_items_filter_unchanged(
        self, stashes: list[Stash], redis_cache: redis.Redis
    ) -> tuple[list[CacheItemWithContext], list[PoeItem], list[PoeItem]]:
        # TODO what if league can change but id stays the same
        not_empty_stash_ids = [stash.id for stash in stashes]

        not_empty_cached_stashes = self._get_cached_stashes(
            redis_cache, not_empty_stash_ids
        )

        changed_items = list[PoeItem]()
        new_items = list[PoeItem]()
        removed_items = list[CacheItemWithContext]()

        n_stashes_cached = 0
        n_items_filtered = 0

        stashes_to_cache = dict[str, CacheStash]()
        for cached_stash, stash in zip(not_empty_cached_stashes, stashes, strict=True):
            cached_stash_changed = False
            if cached_stash is not None:
                n_stashes_cached += 1
                for cached_item in cached_stash.items[:]:
                    idx, new_item = stash.get_item(cached_item.id)
                    if new_item is None:
                        # a cached item doesnt exist anymore
                        cached_stash_changed = True
                        cached_stash.items.remove(cached_item)
                        removed_items.append(
                            CacheItemWithContext(
                                id=cached_item.id,
                                note=cached_item.note,
                                category=cached_item.category,
                                league=stash.league,
                            )
                        )
                        continue
                    if new_item.note == cached_item.note:
                        # Duplicate found in cache
                        n_items_filtered += 1
                        stash.items.pop(idx)
                        continue

                    # PoeItem has changed from cache
                    changed_items.append(new_item)
                    cached_stash_changed = True
                    cached_stash.items.remove(cached_item)

                cached_stash.items.extend(stash.to_cache(self).items)

            else:
                # The stash has never been cached
                cached_stash_changed = True
                cached_stash = stash.to_cache(self)

            new_items.extend(stash.items)

            if cached_stash_changed and cached_stash.items:
                stashes_to_cache[f"stash:{stash.id}"] = cached_stash

        if stashes_to_cache:
            self.local_cache.update(stashes_to_cache)
            redis_cache.mset(stashes_to_cache)

        logger.info(
            f"task=find_changed_filter_unchanged n_stashes_in={len(stashes)} n_stashes_cached={n_stashes_cached} n_items_filtered={n_items_filtered} n_removed_items={len(removed_items)} n_changed_items={len(changed_items)} n_new_items={len(new_items)}"
        )
        return removed_items, changed_items, new_items

    def _organize_items(
        self,
        removed_items: list[CacheItemWithContext],
        changed_items: list[PoeItem],
        new_items: list[PoeItem],
    ) -> OrganizedItemsByCategory:
        categorized_items = OrganizedItemsByCategory()
        for detector in self.detectors:
            table = OrganizedItems()

            for removed_item in removed_items[:]:
                if detector.identifier == removed_item.category:
                    table.removed_items.append(removed_item)
                    removed_items.remove(removed_item)

            for changed_item in changed_items[:]:
                if detector.matches_category(changed_item):
                    table.changed_items.append(changed_item)
                    changed_items.remove(changed_item)

            for new_item in new_items[:]:
                if detector.matches_category(new_item):
                    table.new_items.append(new_item)
                    new_items.remove(new_item)

            setattr(categorized_items, detector.identifier, table)

        return categorized_items

    def get_category(self, item: PoeItem) -> str:
        for detector in self.detectors:
            if detector.matches_category(item):
                return detector.identifier

        raise ValueError("PoeItem does not match a detector category")

    @sync_timing_tracker
    def filter_stashes(
        self, stashes: list[Stash], redis_cache: redis.Redis
    ) -> OrganizedItemsByCategory:
        """
        Parameters:
            :param stashes: a list of stash objects
            :param redis_cache: a redis cache
        Returns:
            :Removed items: items which need to be closed
            :Changed items: items which need to start a new entry
            :New items: items which need to be entered into the system
        """
        stashes = self._filter_duplicates(stashes)

        filtered_stashes, empty_stashes = self._filter_never_used(stashes)
        empty_stash_ids = [stash.id for stash in empty_stashes]

        (
            interesting_stashes,
            no_cache_new_items,
            uninteresting_stashes,
        ) = self._filter_uninteresting_items(filtered_stashes)
        empty_stash_ids.extend([stash.id for stash in uninteresting_stashes])

        removed_items = self._find_removed_items(empty_stash_ids, redis_cache)

        (
            more_removed_items,
            changed_items,
            more_new_items,
        ) = self._find_changed_items_filter_unchanged(interesting_stashes, redis_cache)

        new_items = no_cache_new_items + more_new_items
        removed_items.extend(more_removed_items)

        logger.info(
            f"task=total n_removed_items={len(removed_items)} n_changed_items={len(changed_items)} n_new_items={len(new_items)}"
        )

        return self._organize_items(removed_items, changed_items, new_items)


if __name__ == "__main__":
    import json

    from data_retrieval_app.external_data_retrieval.detectors.unique_detector import (
        UnidentifiedUniqueDetector,
        UniqueDetector,
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
            UniqueDetector(),
            UnidentifiedUniqueDetector(),
        ],
        [{"name": "Standard"}, {"name": "Hardcore"}, {"name": "Allflame"}],
        redis_cache=RedisCacheDecoy(),
    )

    detector_controller.local_cache[
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
