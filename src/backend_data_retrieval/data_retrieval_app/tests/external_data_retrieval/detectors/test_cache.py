from collections.abc import Callable

from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.internal.cache import (
    CacheStash,
)
from data_retrieval_app.external_data_retrieval.detectors.cache import (
    DetectedStashesCache,
)


class TestDetectedStashesCache:
    def test_format_stash_id(self, stashes_cache: DetectedStashesCache) -> None:
        assert stashes_cache._format_stash_id("123") == "stash:123"

    def test_get_local_stashes_returns_cached_stashes(
        self,
        stashes_cache: DetectedStashesCache,
        make_cache_stash: Callable[..., tuple[str, CacheStash]],
    ) -> None:
        stash_id, stash = make_cache_stash()
        formatted_id = stashes_cache._format_stash_id(stash_id)
        stashes_cache.local_cache[formatted_id] = stash

        cached, missing = stashes_cache._get_local_stashes([stash_id, "-1"])

        assert cached[0] == stash
        assert cached[1] is None
        assert missing == [(1, "-1")]

    def test_get_local_stashes_all_cached(
        self,
        stashes_cache: DetectedStashesCache,
        make_cache_stash: Callable[..., tuple[str, CacheStash]],
    ) -> None:
        first_id, first = make_cache_stash()
        second_id, second = make_cache_stash()

        formatted_first_id = stashes_cache._format_stash_id(first_id)
        formatted_second_id = stashes_cache._format_stash_id(second_id)

        stashes_cache.local_cache[formatted_first_id] = first
        stashes_cache.local_cache[formatted_second_id] = second

        cached, missing = stashes_cache._get_local_stashes([first_id, second_id])

        assert cached == [first, second]
        assert missing == []

    def test_get_local_stashes_all_missing(
        self,
        stashes_cache: DetectedStashesCache,
    ) -> None:
        cached, missing = stashes_cache._get_local_stashes(["-1", "-2"])

        assert cached == [None, None]
        assert missing == [(0, "-1"), (1, "-2")]

    def test_get_redis_stashes_fills_missing_entries(
        self,
        stashes_cache: DetectedStashesCache,
        make_cache_stash: Callable[..., tuple[str, CacheStash]],
    ) -> None:
        stash_id, stash = make_cache_stash()
        formatted_id = stashes_cache._format_stash_id(stash_id)
        stashes_cache.redis_cache.set(formatted_id, stash.model_dump_json())

        cached = [None, None]
        missing = [(0, stash_id), (1, "456")]

        result = stashes_cache._get_redis_stashes(cached, missing)

        assert result == [stash, None]

    def test_get_redis_stashes_preserves_local_entries(
        self,
        stashes_cache: DetectedStashesCache,
        make_cache_stash: Callable[..., tuple[str, CacheStash]],
    ) -> None:
        _, local_stash = make_cache_stash()
        redis_stash_id, redis_stash = make_cache_stash()

        formatted_redis_stash_id = stashes_cache._format_stash_id(redis_stash_id)

        stashes_cache.redis_cache.set(
            formatted_redis_stash_id, redis_stash.model_dump_json()
        )

        cached = [local_stash, None]
        missing = [(1, redis_stash_id)]

        result = stashes_cache._get_redis_stashes(cached, missing)

        assert result == [local_stash, redis_stash]

    def test_get_redis_stashes_with_no_missing_entries(
        self,
        stashes_cache: DetectedStashesCache,
        make_cache_stash: Callable[..., tuple[str, CacheStash]],
    ) -> None:
        _, stash = make_cache_stash()

        result = stashes_cache._get_redis_stashes([stash], [])

        assert result == [stash]

    def test_get_stashes_returns_empty_list_for_empty_ids(
        self,
        stashes_cache: DetectedStashesCache,
    ) -> None:
        assert stashes_cache.get_stashes([]) == []

    def test_get_stashes_reads_from_redis(
        self,
        stashes_cache: DetectedStashesCache,
        make_cache_stash: Callable[..., tuple[str, CacheStash]],
    ) -> None:
        stash_id, stash = make_cache_stash()
        formatted_id = stashes_cache._format_stash_id(stash_id)
        stashes_cache.redis_cache.set(formatted_id, stash.model_dump_json())

        result = stashes_cache.get_stashes([stash_id])

        assert result == [stash]

    def test_get_stashes_prefers_local_cache(
        self,
        stashes_cache: DetectedStashesCache,
        make_cache_stash: Callable[..., tuple[str, CacheStash]],
    ) -> None:
        stash_id, stash = make_cache_stash()
        formatted_id = stashes_cache._format_stash_id(stash_id)
        stashes_cache.local_cache[formatted_id] = stash

        result = stashes_cache.get_stashes([stash_id])

        assert result == [stash]

    def test_get_stashes_preserves_input_order(
        self,
        stashes_cache: DetectedStashesCache,
        make_cache_stash: Callable[..., tuple[str, CacheStash]],
    ) -> None:
        first_id, first = make_cache_stash()
        third_id, third = make_cache_stash()

        formatted_first_id = stashes_cache._format_stash_id(first_id)
        formatted_third_id = stashes_cache._format_stash_id(third_id)

        stashes_cache.local_cache[formatted_first_id] = first
        stashes_cache.redis_cache.set(formatted_third_id, third.model_dump_json())

        result = stashes_cache.get_stashes([first_id, "-2", third_id])

        assert result == [first, None, third]

    def test_remove_stashes_removes_from_both_caches(
        self,
        stashes_cache: DetectedStashesCache,
        make_cache_stash: Callable[..., tuple[str, CacheStash]],
    ) -> None:
        stash_id, stash = make_cache_stash()
        formatted_id = stashes_cache._format_stash_id(stash_id)

        stashes_cache.local_cache[formatted_id] = stash
        stashes_cache.redis_cache.set(formatted_id, stash.model_dump_json())

        stashes_cache.remove_stashes([stash_id])

        assert formatted_id not in stashes_cache.local_cache
        assert stashes_cache.redis_cache.get(formatted_id) is None

    def test_remove_stashes_ignores_missing_keys(
        self,
        stashes_cache: DetectedStashesCache,
        make_cache_stash: Callable[..., tuple[str, CacheStash]],
    ) -> None:
        stash_id, stash = make_cache_stash()
        formatted_id = stashes_cache._format_stash_id(stash_id)

        stashes_cache.local_cache[formatted_id] = stash

        stashes_cache.remove_stashes(["missing"])

        assert stashes_cache.local_cache == {formatted_id: stash}
        assert stashes_cache.redis_cache.get("stash:missing") is None

    def test_update_stashes_serializes_stashes(
        self,
        stashes_cache: DetectedStashesCache,
        make_cache_stash: Callable[..., tuple[str, CacheStash]],
    ) -> None:
        stash_id, stash = make_cache_stash()
        formatted_id = stashes_cache._format_stash_id(stash_id)

        stashes_cache.update_stashes({stash_id: stash})

        assert stashes_cache.local_cache[formatted_id] == stash

    def test_update_stashes_does_not_write_to_redis(
        self,
        stashes_cache: DetectedStashesCache,
        make_cache_stash: Callable[..., tuple[str, CacheStash]],
    ) -> None:
        stash_id, stash = make_cache_stash()
        formatted_id = stashes_cache._format_stash_id(stash_id)

        stashes_cache.update_stashes({stash_id: stash})

        assert stashes_cache.redis_cache.get(formatted_id) is None
