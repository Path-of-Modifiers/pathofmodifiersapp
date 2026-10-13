import json
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
from data_retrieval_app.external_data_retrieval.detectors.cache import (
    DetectedStashesCache,
)
from data_retrieval_app.external_data_retrieval.utils import (
    sync_timing_tracker,
)
from data_retrieval_app.logs.logger import data_retrieval_logger as logger


class DetectorController:
    backend_base_url = settings.BACKEND_BASE_URL

    def __init__(
        self,
        detectors: list[CategoryDetectorBase],
        leagues: list[League],
    ):
        self.leagues = [league.name for league in leagues]

        self.detectors = detectors

        self.cache = DetectedStashesCache()
        self.redis_cache_set = False

    def set_redis_cache(self, redis_cache: redis.Redis):
        self.cache.set_redis_cache(redis_cache)
        self.redis_cache_set = True

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

        logger.info(
            f"task=filter_duplicates n_stashes_in={len(stashes)} n_duplicate_stashes={duplicates_found}"
        )
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
            found_items = False
            for detector in self.detectors:
                # the donor stash is modified inplace, with its items moving over to the receiver stashes inplace
                found_items = (
                    detector.find_interesting_items(
                        donor_stash, receiver_stash, no_cache_receiver_stash
                    )
                    or found_items
                )

            if found_items:
                if receiver_stash.items:
                    interesting_stashes.append(receiver_stash)

                if no_cache_receiver_stash.items:
                    # items such as unidentified items
                    no_cache_new_items.extend(no_cache_receiver_stash.items)
            else:
                n_uninteresting_items += len(donor_stash.items)

                filtered_stashes.append(donor_stash)

        logger.info(
            f"task=filter_uninteresting n_stashes_in={len(stashes)} n_stashes_filtered={len(filtered_stashes)} n_items_in={n_items_in} n_items_filtered={n_uninteresting_items}"
        )
        return interesting_stashes, no_cache_new_items, filtered_stashes

    def _find_removed_items(
        self, empty_stash_ids: list[str]
    ) -> list[CacheItemWithContext]:
        # TODO what if league can change but id stays the same
        empty_cached_stashes = self.cache.get_stashes(empty_stash_ids)
        removed_items = list[CacheItemWithContext]()
        cached_stashes_to_remove = list[str]()

        for id, cached_stash in zip(empty_stash_ids, empty_cached_stashes, strict=True):
            if cached_stash is None:
                continue

            cached_stashes_to_remove.append(id)
            for cached_item in cached_stash.items:
                removed_items.append(
                    CacheItemWithContext(
                        **cached_item.model_dump(), league=cached_stash.league
                    )
                )

        if cached_stashes_to_remove:
            self.cache.remove_stashes(cached_stashes_to_remove)

        logger.info(
            f"task=find_removed n_stashes_in={len(empty_stash_ids)} n_stashes_cached={len(cached_stashes_to_remove)} n_removed_items={len(removed_items)}"
        )
        return removed_items

    def _find_changed_items_filter_unchanged(
        self, stashes: list[Stash]
    ) -> tuple[list[CacheItemWithContext], list[PoeItem], list[PoeItem]]:
        # TODO what if league can change but id stays the same
        not_empty_stash_ids = [stash.id for stash in stashes]

        not_empty_cached_stashes = self.cache.get_stashes(not_empty_stash_ids)

        changed_items = list[PoeItem]()
        new_items = list[PoeItem]()
        removed_items = list[CacheItemWithContext]()

        n_stashes_cached = 0
        n_items_filtered = 0

        stashes_to_cache = dict[str, CacheStash]()
        for cached_stash, current_stash in zip(
            not_empty_cached_stashes, stashes, strict=True
        ):
            cached_stash_changed = False
            if cached_stash is not None:
                # The stash has previously been cached
                n_stashes_cached += 1
                (
                    n_more_items_filtered,
                    more_removed_items,
                    more_changed_items,
                    more_new_items,
                ) = self.cache.separate_cached_items(current_stash, cached_stash)
                n_items_filtered += n_more_items_filtered

                cached_stash.items = [
                    item.to_cache(self) for item in (more_new_items + more_new_items)
                ]

                removed_items.extend(more_removed_items)
                changed_items.extend(more_changed_items)
                new_items.extend(more_new_items)

                if more_removed_items or more_changed_items or more_new_items:
                    cached_stash_changed = True

            else:
                # The stash has never been cached
                cached_stash_changed = True
                cached_stash = current_stash.to_cache(self)

                # All items must be new
                new_items.extend(current_stash.items)

            if cached_stash_changed and cached_stash.items:
                stashes_to_cache[current_stash.id] = cached_stash

        if stashes_to_cache:
            self.cache.update_stashes(stashes_to_cache)

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
    def filter_stashes(self, stashes: list[Stash]) -> OrganizedItemsByCategory:
        """
        Parameters:
            :param stashes: a list of stash objects
            :param redis_cache: a redis cache
        Returns:
            :Removed items: items which need to be closed
            :Changed items: items which need to start a new entry
            :New items: items which need to be entered into the system
        """
        if not self.redis_cache_set:
            raise RuntimeError(
                "Redis cache has not been set. Call set_redis_cache() first."
            )

        stashes = self._filter_duplicates(stashes)

        filtered_stashes, empty_stashes = self._filter_never_used(stashes)
        empty_stash_ids = [stash.id for stash in empty_stashes]

        (
            interesting_stashes,
            no_cache_new_items,
            uninteresting_stashes,
        ) = self._filter_uninteresting_items(filtered_stashes)
        empty_stash_ids.extend([stash.id for stash in uninteresting_stashes])

        removed_items = self._find_removed_items(empty_stash_ids)

        (
            more_removed_items,
            changed_items,
            more_new_items,
        ) = self._find_changed_items_filter_unchanged(interesting_stashes)

        new_items = no_cache_new_items + more_new_items
        removed_items.extend(more_removed_items)

        logger.info(
            f"task=total n_removed_items={len(removed_items)} n_changed_items={len(changed_items)} n_new_items={len(new_items)}"
        )

        return self._organize_items(removed_items, changed_items, new_items)

    # def post_transform_cleanup(self, organized_items: OrganizedItemsByCategory):
    #     dismissed_items_by_cached_stash = defaultdict[str, list[PoeItem]]()
    #     for category in organized_items.iter_categories():
    #         for dimissed_item in category.dismissed_items:
    #             cached_stash_id = self.item_id_to_cached_stash_id[dimissed_item.id]
    #             dismissed_items_by_cached_stash[cached_stash_id].append(dimissed_item)

    #     for cached_stash_id, dimissed_items in dismissed_items_by_cached_stash.items():
    #         cached_stash = self.cached_stash_adapter.validate_json(
    #             self.local_cache[cached_stash_id]
    #         )
    #         for item in dimissed_items:
    #             cached_stash.items.remove(item)

    def end_of_program_cleanup(self):
        self.cache.flush_local_cache()


if __name__ == "__main__":
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
