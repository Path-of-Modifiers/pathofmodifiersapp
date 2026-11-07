from collections.abc import Callable
from datetime import UTC, datetime
from unittest.mock import patch

import pytest
import redis
from backend_api.app.core.schemas.currency import Currency
from backend_api.app.core.schemas.league import League

from data_retrieval_app.external_data_retrieval.cache import (
    get_cache,
)
from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.internal.cache import (
    CacheItem,
    CacheStash,
)
from data_retrieval_app.external_data_retrieval.detectors.cache import (
    DetectedStashesCache,
)
from data_retrieval_app.external_data_retrieval.detectors.detector_controller import (
    DetectorController,
)
from data_retrieval_app.external_data_retrieval.detectors.unique_detector import (
    UniqueDetector,
)
from data_retrieval_app.external_data_retrieval.transforming_data.transform_poe_api_data import (
    PoEAPIDataTransformer,
)
from data_retrieval_app.pom_api_authentication import get_superuser_token_headers
from data_retrieval_app.tests.external_data_retrieval.utils import (
    get_bases,
    get_icons,
    get_uniques,
    get_wanted_item,
    make_id,
    make_random_league,
    make_valid_note,
)
from data_retrieval_app.tests.external_data_retrieval.utils.item_factory import (
    PoEItemFactory,
)
from data_retrieval_app.tests.scripts.create_public_stashes_test_data.config import (
    script_settings,
)
from data_retrieval_app.utils import get_grouped_modifiers_by_unique


@pytest.fixture(scope="session")
def pom_auth_headers():
    base_url = settings.BACKEND_BASE_URL
    return get_superuser_token_headers(base_url)


@pytest.fixture(scope="function")
def mock_cache():
    with patch(
        "data_retrieval_app.external_data_retrieval.config.settings.REDIS_BACKEND_DATA_RETRIEVAL",
        15,
    ):
        with get_cache() as cache:
            cache.flushdb()
            yield cache
            cache.flushdb()


@pytest.fixture(scope="session")
def leagues() -> list[League]:
    league_names = script_settings.LEAGUES
    leagues = list[League]()
    for league_id, name in enumerate(league_names):
        leagues.append(
            League(
                name=name, validFrom=datetime.now(UTC), version=3.29, leagueId=league_id
            )
        )
    return leagues


@pytest.fixture(scope="session")
def league_id_by_name(leagues: list[League]) -> dict[str, int]:
    return {league.name: league.leagueId for league in leagues}


@pytest.fixture(scope="session")
def currencies(league_id_by_name: dict[str, int]) -> dict[tuple[int, str], Currency]:
    currency_types = script_settings.ITEM_NOTE_CURRENCY_TYPES + ["mirror"]
    currencies = dict[tuple[int, str], Currency]()
    for league_id in league_id_by_name.values():
        for i, cur_type in enumerate(currency_types):
            currencies[(league_id, cur_type)] = Currency(
                currencyId=i,
                tradeName=cur_type,
                name=f"{cur_type.capitalize()} Orb",
                createdHoursSinceLaunch=-1,
                valueInChaos=i * 10,
                leagueId=league_id,
            )

    return currencies


@pytest.fixture(scope="session")
def modifiers_by_unique(pom_auth_headers) -> dict:
    return get_grouped_modifiers_by_unique(pom_auth_headers)


@pytest.fixture(scope="session")
def uniques(modifiers_by_unique) -> dict:
    return get_uniques(modifiers_by_unique)


@pytest.fixture(scope="session")
def bases(pom_auth_headers) -> dict:
    return get_bases(pom_auth_headers)


@pytest.fixture(scope="session")
def icons() -> dict:
    return get_icons()


@pytest.fixture(scope="session")
def item_factory(modifiers_by_unique, uniques, bases, icons, leagues):
    return PoEItemFactory(modifiers_by_unique, uniques, bases, icons, leagues)


@pytest.fixture(scope="session")
def ctx_assembler() -> Callable[..., dict]:
    def _ctx_assembler(*all_ctx: dict) -> dict:
        assembled = {}
        for ctx in all_ctx:
            assembled.update(ctx)

        return assembled

    return _ctx_assembler


@pytest.fixture(scope="session")
def ctx_unique() -> dict:
    return {"rarity": "Unique"}


@pytest.fixture
def ctx_valid_note() -> dict:
    return {"note": make_valid_note()}


@pytest.fixture(scope="session")
def ctx_invalid_note() -> dict:
    return {"note": "no price"}


@pytest.fixture(scope="session")
def ctx_uninteresting_fields_are_none(detector_controller: DetectorController) -> dict:
    return dict.fromkeys(detector_controller.uninteresting_item_fields)


@pytest.fixture(scope="session")
def unique_detector():
    return UniqueDetector()


@pytest.fixture(scope="function")
def ctx_wanted_item(unique_detector: UniqueDetector):
    wanted_item = get_wanted_item(unique_detector)

    return {"name": wanted_item}


@pytest.fixture(scope="function")
def ctx_unwanted_item(unique_detector: UniqueDetector):
    wanted_item = get_wanted_item(unique_detector)

    return {"name": "unwated_" + wanted_item}


@pytest.fixture(scope="session")
def data_transformer(
    leagues,
    currencies,
) -> PoEAPIDataTransformer:
    data_transformer = PoEAPIDataTransformer(leagues)
    data_transformer.set_currencies(currencies)
    return data_transformer


@pytest.fixture(scope="session")
def detector_controller(
    unique_detector, leagues, data_transformer
) -> DetectorController:
    return DetectorController(
        [
            unique_detector,
            # UnidentifiedUniqueDetector(),
        ],
        leagues,
        data_transformer,
    )


@pytest.fixture
def stashes_cache(mock_cache: redis.Redis) -> DetectedStashesCache:
    cache = DetectedStashesCache()
    cache.set_redis_cache(mock_cache)
    return cache


@pytest.fixture
def make_cache_item() -> Callable[..., CacheItem]:
    def _make_cache_item(**ctx) -> CacheItem:
        ctx.setdefault("id", make_id())
        ctx.setdefault("note", make_valid_note())
        ctx.setdefault("category", "unique")

        return CacheItem.model_validate(ctx)

    return _make_cache_item


@pytest.fixture
def make_cache_stash(make_cache_item) -> Callable[..., tuple[str, CacheStash]]:
    def _make_cache_stash(*, n_items: int = 1, **ctx) -> tuple[str, CacheStash]:
        cache_id = ctx.pop("id", None)
        if cache_id is None:
            cache_id = make_id()

        league = ctx.pop("items", None)
        if league is None:
            league = make_random_league()

        items = ctx.pop("items", None)
        if items is None:
            items = []

        made_items = []
        for item_ctx in items:
            made_items.append(make_cache_item(**item_ctx))

        while len(made_items) < n_items:
            made_items.append(make_cache_item())

        return cache_id, CacheStash(league=league, items=made_items)

    return _make_cache_stash
