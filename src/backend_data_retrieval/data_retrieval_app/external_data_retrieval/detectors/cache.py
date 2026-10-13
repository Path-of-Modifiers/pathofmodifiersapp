import redis
from pydantic import TypeAdapter

from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.external.poe import (
    PoeItem,
    Stash,
)
from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.internal.cache import (
    CacheItemWithContext,
    CacheStash,
)


class DetectedStashesCache:
    def __init__(self):
        self.local_cache = dict[str, str]()
        self.redis_cache = None

        self.cached_stash_adapter = TypeAdapter(CacheStash)

    def set_redis_cache(self, redis_cache: redis.Redis):
        self.redis_cache = redis_cache

    @staticmethod
    def _format_stash_id(id: str) -> str:
        return f"stash:{id}"

    def _get_local_stashes(
        self, ids: list[str]
    ) -> tuple[list[CacheStash | None], list[tuple[int, str]]]:
        cached_stashes = list[CacheStash | None]()
        still_needs_check = list[tuple[int, str]]()
        for i, id in enumerate(ids):
            cached_stash = self.local_cache.get(self._format_stash_id(id))
            if cached_stash is None:
                still_needs_check.append((i, id))
                cached_stashes.append(None)
            else:
                cached_stashes.append(
                    self.cached_stash_adapter.validate_json(cached_stash)
                )

        return cached_stashes, still_needs_check

    def _get_redis_stashes(
        self,
        cached_stashes: list[CacheStash | None],
        still_needs_check: list[tuple[int, str]],
    ) -> list[CacheStash | None]:
        redis_cached_stashes: list[str | None] = self.redis_cache.mget(
            [self._format_stash_id(id) for _, id in still_needs_check]
        )
        for i, cached_stash in enumerate(redis_cached_stashes):
            if cached_stash is not None:
                idx, _ = still_needs_check[i]
                cached_stashes[idx] = self.cached_stash_adapter.validate_json(
                    cached_stash
                )

        return cached_stashes

    def separate_cached_items(
        self, current_stash: Stash, cached_stash: CacheStash
    ) -> tuple[int, list[CacheItemWithContext], list[PoeItem], list[PoeItem]]:
        """
        Separates items in the current cached into removed, changed, and new.
        Returns:
            n_items_filtered: (int) number of unchanged items
            removed_items: (list[CacheItemWithContext]) items that are no longer present in the current stash
            changed_items: (list[PoeItem]) items with a different price
            new_items: (list[PoeItem]) items not present in cache
        """
        removed_items = list[CacheItemWithContext]()
        changed_items = list[PoeItem]()
        new_items = current_stash.items

        n_items_filtered = 0
        for cached_item in cached_stash.items:
            item = current_stash.get_item(cached_item.id)
            if item is None:
                # a cached item doesnt exist anymore
                removed_items.append(
                    CacheItemWithContext(
                        id=cached_item.id,
                        note=cached_item.note,
                        category=cached_item.category,
                        league=current_stash.league,
                    )
                )
            else:
                # Item has been previously cached -> not new
                new_items.remove(item)
                if item.note == cached_item.note:
                    # Duplicate found in cache
                    n_items_filtered += 1
                else:
                    # PoeItem has changed from cache
                    changed_items.append(item)

        return (
            n_items_filtered,
            removed_items,
            changed_items,
            new_items,
        )

    def get_stashes(self, ids: list[str]) -> list[CacheStash | None]:
        """
        First checks local cache, then redis cache. This method relies on the local cache
        being exactly aligned with the redis cache for stashes that exists in both.
        """
        if len(ids) == 0:
            return []

        cached_stashes, still_needs_check = self._get_local_stashes(ids)
        cached_stashes = self._get_redis_stashes(cached_stashes, still_needs_check)

        return cached_stashes

    def remove_stashes(self, ids: list[str]):
        formatted_ids = [self._format_stash_id(id) for id in ids]
        [self.local_cache.pop(id, None) for id in formatted_ids]
        self.redis_cache.delete(*formatted_ids)

    def update_stashes(self, stashes: dict[str, CacheStash]):
        for id, stash in stashes.items():
            self.local_cache[self._format_stash_id(id)] = stash.model_dump_json()

    def flush_local_cache(self):
        if self.local_cache:
            self.redis_cache.mset(self.local_cache)
