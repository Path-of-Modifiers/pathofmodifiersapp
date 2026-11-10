from collections.abc import Callable
from unittest.mock import patch

import pytest

from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.external.poe import (
    PoeItem,
    Stash,
)
from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.internal.cache import (
    CacheStash,
)
from data_retrieval_app.external_data_retrieval.detectors.detector_controller import (
    DetectorController,
)
from data_retrieval_app.tests.external_data_retrieval.utils import (
    make_id,
    make_random_league,
    make_valid_note,
)
from data_retrieval_app.tests.external_data_retrieval.utils.item_factory import (
    PoEItemFactory,
)


@pytest.fixture
def make_stash() -> Callable[..., Stash]:
    def _make_stash(
        *,
        id: str | None = None,
        public: bool = True,
        items: list[PoeItem] | None = None,
        league: str | None = None,
        name: str | None = None,
        stash_type: str = "TradeStash",
    ) -> Stash:
        if id is None:
            id = make_id()
        if items is None:
            items = []
        if league is None:
            league = make_random_league()

        return Stash(
            id=id,
            public=public,
            stash=name,
            stashType=stash_type,
            league=league,
            items=items,
        )

    return _make_stash


class TestDetectorController:
    def test_filter_duplicate_stashes(
        self, detector_controller: DetectorController, make_stash
    ):
        stash = make_stash()
        stashes = [stash, stash]

        filtered_stashes = detector_controller._filter_duplicate_stashes(stashes)
        assert len(filtered_stashes) == 1
        assert filtered_stashes[0] == stash

    def test_filter_duplicate_stashes_does_nothing(
        self, detector_controller: DetectorController, make_stash
    ):
        stash = make_stash()
        stashes = [stash]

        filtered_stashes = detector_controller._filter_duplicate_stashes(stashes)
        assert len(filtered_stashes) == 1
        assert filtered_stashes[0] == stash

    def test_filter_duplicate_stashes_correct_priority(
        self, detector_controller: DetectorController, make_stash
    ):
        stash = make_stash()
        stash_2 = make_stash()
        stash_2.id = stash.id
        stashes = [stash, stash_2]

        filtered_stashes = detector_controller._filter_duplicate_stashes(stashes)
        assert len(filtered_stashes) == 1
        assert filtered_stashes[0] == stash_2

    def test_filter_never_used_public_or_league(self):
        # TODO test league migration
        pass

    def test_filter_never_used_no_price(
        self,
        detector_controller: DetectorController,
        item_factory: PoEItemFactory,
        make_stash,
        ctx_assembler,
        ctx_uninteresting_fields_are_none,
        ctx_invalid_note,
    ):
        ctx = ctx_assembler(ctx_uninteresting_fields_are_none, ctx_invalid_note)
        item = item_factory.create(ctx=ctx)
        stash = make_stash(items=[item])
        stashes = [stash]

        filtered_stashes, empty_stashes = detector_controller._filter_never_used(
            stashes
        )

        assert not filtered_stashes
        assert empty_stashes == stashes

    def test_filter_never_used_stash_price(
        self,
        detector_controller: DetectorController,
        item_factory: PoEItemFactory,
        make_stash,
        ctx_assembler,
        ctx_uninteresting_fields_are_none,
        ctx_invalid_note,
    ):
        ctx = ctx_assembler(ctx_uninteresting_fields_are_none, ctx_invalid_note)
        item = item_factory.create(ctx=ctx)
        stash_note = make_valid_note()
        stash = make_stash(items=[item], name=stash_note)
        stashes = [stash]

        filtered_stashes, empty_stashes = detector_controller._filter_never_used(
            stashes
        )

        assert not empty_stashes
        assert len(filtered_stashes) == 1
        assert filtered_stashes[0].items
        assert filtered_stashes[0].items[0].note == stash_note

    def test_filter_never_used_valid_price(
        self,
        detector_controller: DetectorController,
        item_factory: PoEItemFactory,
        make_stash,
        ctx_assembler,
        ctx_valid_note,
        ctx_uninteresting_fields_are_none,
    ):
        ctx = ctx_assembler(ctx_valid_note, ctx_uninteresting_fields_are_none)
        item = item_factory.create(ctx=ctx)
        stash = make_stash(items=[item])
        stashes = [stash]

        filtered_stashes, empty_stashes = detector_controller._filter_never_used(
            stashes
        )

        assert not empty_stashes
        assert len(filtered_stashes) == 1
        assert filtered_stashes[0].items
        assert filtered_stashes[0].items[0] == item

    def test_filter_never_used_empty_stash(
        self,
        detector_controller: DetectorController,
        make_stash,
    ):
        stash = make_stash()
        stashes = [stash]

        filtered_stashes, empty_stashes = detector_controller._filter_never_used(
            stashes
        )

        assert not filtered_stashes
        assert len(empty_stashes) == 1
        assert empty_stashes[0].id == stash.id
        assert not empty_stashes[0].items

    def test_filter_uninteresting_items_interesting(
        self,
        detector_controller: DetectorController,
        item_factory: PoEItemFactory,
        make_stash,
        ctx_assembler,
        ctx_unique,
        ctx_valid_note,
        ctx_wanted_item,
    ):
        ctx = ctx_assembler(ctx_unique, ctx_wanted_item, ctx_valid_note)
        item = item_factory.create(ctx=ctx)

        stash = make_stash(items=[item])
        stashes = [stash]

        (
            interesting_stashes,
            no_cache_new_items,
            uninteresting_stashes,
        ) = detector_controller._filter_uninteresting_items(stashes)

        assert len(interesting_stashes) == 1
        assert interesting_stashes[0].id == stash.id
        assert not stash.items
        assert not no_cache_new_items
        assert not uninteresting_stashes

    def test_filter_uninteresting_items_interesting_no_cache(
        self,
        detector_controller: DetectorController,
        item_factory: PoEItemFactory,
        make_stash,
        ctx_assembler,
        ctx_unique,
        ctx_valid_note,
        ctx_wanted_item,
    ):
        # TODO when implementing unidentified items
        pass

    def test_filter_uninteresting_items_uninteresting(
        self,
        detector_controller: DetectorController,
        item_factory: PoEItemFactory,
        make_stash,
        ctx_assembler,
        ctx_unique,
        ctx_valid_note,
        ctx_unwanted_item,
    ):
        ctx = ctx_assembler(ctx_unique, ctx_unwanted_item, ctx_valid_note)
        item = item_factory.create(ctx=ctx)

        stash = make_stash(items=[item])
        stashes = [stash]

        (
            interesting_stashes,
            no_cache_new_items,
            uninteresting_stashes,
        ) = detector_controller._filter_uninteresting_items(stashes)

        assert not interesting_stashes
        assert not no_cache_new_items
        assert len(uninteresting_stashes) == 1
        assert uninteresting_stashes[0] == stash

    def test_find_removed_items(
        self,
        detector_controller: DetectorController,
        make_cache_stash: Callable[..., tuple[str, CacheStash]],
    ):
        cached_stash_id, cached_stash = make_cache_stash()
        not_cached_stash_id = make_id()
        empty_stash_ids = [cached_stash_id, not_cached_stash_id]

        with patch.object(
            detector_controller.cache, "get_stashes", return_value=[cached_stash, None]
        ), patch.object(detector_controller.cache, "remove_stashes") as mock_remove:
            removed_items = detector_controller._find_removed_items(empty_stash_ids)
            mock_remove.assert_called_once_with([cached_stash_id])

        assert len(removed_items) == 1
        removed_item = removed_items[0]
        cached_item = cached_stash.items[0]
        assert removed_item.id == cached_item.id
        assert removed_item.category == cached_item.category
        assert removed_item.note == cached_item.note
        assert removed_item.league == cached_stash.league

    def test_find_removed_items_removes_cached_stashes(
        self,
        detector_controller: DetectorController,
        make_cache_stash: Callable[..., tuple[str, CacheStash]],
    ):
        cached_stash_id, cached_stash = make_cache_stash()
        empty_stash_ids = [cached_stash_id]

        with patch.object(
            detector_controller.cache, "get_stashes", return_value=[cached_stash]
        ), patch.object(detector_controller.cache, "remove_stashes") as mock_remove:
            removed_items = detector_controller._find_removed_items(empty_stash_ids)
            mock_remove.assert_called_once_with(empty_stash_ids)

        # mock_remove.assert_called_once_with(["stash-1"])
        assert len(removed_items) == 1

        removed_item = removed_items[0]
        cached_item = cached_stash.items[0]
        assert removed_item.id == cached_item.id
        assert removed_item.category == cached_item.category
        assert removed_item.note == cached_item.note
        assert removed_item.league == cached_stash.league

    def test_find_removed_items_no_cached_stashes(
        self,
        detector_controller: DetectorController,
    ):
        # empty_stash_ids = ["stash-1"]
        empty_stash_ids = [make_id()]

        with patch.object(
            detector_controller.cache, "get_stashes", return_value=[None]
        ), patch.object(detector_controller.cache, "remove_stashes") as mock_remove:
            removed_items = detector_controller._find_removed_items(empty_stash_ids)

            mock_remove.assert_not_called()

        assert not removed_items

    def test_process_previously_cached_stash(
        self,
        detector_controller: DetectorController,
        item_factory: PoEItemFactory,
        make_stash,
    ):
        stash_id = make_id()
        league = make_random_league()

        item_removed = item_factory.create()
        item_unchanged_removed = item_factory.create()
        item_new = item_factory.create()

        item_changed_1 = item_factory.create()
        item_changed_1.note = make_valid_note(price=10)
        item_changed_2 = item_changed_1.model_copy()
        item_changed_2.note = make_valid_note(price=11)

        stash = make_stash(
            items=[item_changed_1, item_unchanged_removed, item_new],
            id=stash_id,
            league=league,
        )

        cached_stash = make_stash(
            items=[item_changed_2, item_unchanged_removed, item_removed],
            id=stash_id,
            league=league,
        ).to_cache(detector_controller)

        (
            n_more_items_filtered,
            cached_stash,
            more_removed_items,
            more_changed_items,
            more_new_items,
        ) = detector_controller._process_previously_cached_stash(
            cached_stash.model_copy(), stash
        )

        assert n_more_items_filtered == 1
        assert cached_stash == stash.to_cache(detector_controller)

        assert len(more_removed_items) == 1
        item_removed_from_cache = more_removed_items[0]
        assert item_removed_from_cache == item_removed.to_cache(
            detector_controller
        ).add_context(league)

        assert len(more_changed_items) == 1
        item_changed_from_cache = more_changed_items[0]
        assert item_changed_from_cache == item_changed_1

        assert len(more_new_items) == 1
        item_new_from_cache = more_new_items[0]
        assert item_new_from_cache == item_new

    def test_process_new_stash(
        self,
        detector_controller: DetectorController,
        make_stash,
    ):
        stash = make_stash()

        cached_stash, more_new_items = detector_controller._process_new_stash(stash)
        assert cached_stash == stash.to_cache(detector_controller)
        assert more_new_items == stash.items

    def test_find_changed_items_filter_unchanged(
        self,
        detector_controller: DetectorController,
        item_factory: PoEItemFactory,
        make_stash,
    ):
        item = item_factory.create()

        stash_1 = make_stash(
            items=[item],
        )
        cached_stash = stash_1.to_cache(detector_controller)

        stash_2 = make_stash(items=[item])
        stashes = [stash_1, stash_2]
        with patch.object(
            detector_controller.cache, "get_stashes", return_value=[cached_stash, None]
        ), patch.object(detector_controller.cache, "update_stashes") as mock_update:
            _, _, new_items = detector_controller._find_changed_items_filter_unchanged(
                stashes
            )
            mock_update.assert_called_once_with(
                {stash_2.id: stash_2.to_cache(detector_controller)}
            )

        assert len(new_items) == 1

    def test_filter_stashes_empty_stashes(
        self, detector_controller: DetectorController, mock_cache, make_stash
    ):
        detector_controller.set_redis_cache(mock_cache)
        # test that the right stashes are checked with _find_removed_items
        empty_stash = make_stash()

        stashes = [empty_stash]

        with patch.object(
            detector_controller, "_find_removed_items"
        ) as mock_find_removed_items:
            detector_controller.filter_stashes(stashes)
            mock_find_removed_items.assert_called_once_with([empty_stash.id])
