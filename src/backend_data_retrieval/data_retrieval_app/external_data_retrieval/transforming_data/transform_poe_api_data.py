from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Literal, TypeVar

from backend_api.app.core.schemas.currency import Currency
from backend_api.app.core.schemas.item import (
    ItemAvailabilityExpired,
    ItemAvailabilityUpdated,
    ItemBase,
    ItemCreate,
    ItemPrice,
)
from backend_api.app.core.schemas.item_base_type import ItemBaseType
from backend_api.app.core.schemas.league import League
from backend_api.app.core.schemas.modifier import GroupedModifier
from pydantic import BaseModel, TypeAdapter

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.external.poe import (
    PoeItem,
)
from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.internal.cache import (
    CacheItemWithContext,
)
from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.internal.categorized import (
    OrganizedItems,
    OrganizedItemsByCategory,
)
from data_retrieval_app.external_data_retrieval.detectors.base import (
    CategoryDetectorBase,
)
from data_retrieval_app.external_data_retrieval.detectors.unique_detector import (
    # UnidentifiedUniqueDetector,
    UniqueDetector,
)
from data_retrieval_app.external_data_retrieval.transforming_data.roll_processor import (
    RollProcessor,
)
from data_retrieval_app.external_data_retrieval.utils import sync_timing_tracker
from data_retrieval_app.logs.logger import transform_logger as logger
from data_retrieval_app.pom_api_authentication import get_superuser_token_headers
from data_retrieval_app.utils import send_request_safe


class PoEAPIDataTransformer:
    url = settings.BACKEND_BASE_URL
    pom_auth_headers = get_superuser_token_headers(url)

    def __init__(
        self,
        leagues: list[League],
    ) -> None:
        logger.debug("Initializing PoEAPIDataTransformer")

        self.pom_auth_headers = get_superuser_token_headers(self.url)

        modifiers = self._get_modifiers()
        item_base_types = self._get_item_base_types()

        self.roll_processor = RollProcessor(modifiers)

        self.league_to_id = {league.name: league.leagueId for league in leagues}

        logger.debug("Initializing PoEAPIDataTransformer done.")

        self.transformers: list[TransformerBase] = [
            UniqueTransformer(self.league_to_id, item_base_types, self.roll_processor),
            # UnidentifiedUniqueTransformer(self.league_to_id, item_base_types, self.roll_processor),
        ]

    def _get_modifiers(self) -> dict[str, GroupedModifier]:
        response = send_request_safe(
            "get",
            f"{self.url}/modifier/grouped/",
            headers=self.pom_auth_headers,
            logger=logger,
        )
        modifiers = TypeAdapter(list[GroupedModifier]).validate_python(response.json())

        name_to_modifiers = defaultdict[str, list[GroupedModifier]](list)
        for modifier in modifiers:
            uniques = modifier.relatedUniques.split("|")
            for unique in uniques:
                name_to_modifiers[unique].append(modifier)

        return dict(name_to_modifiers)

    def _get_item_base_types(self) -> dict[str, int]:
        response = send_request_safe(
            "get",
            f"{self.url}/itemBaseType/",
            headers=self.pom_auth_headers,
            logger=logger,
        )

        base_types = TypeAdapter(list[ItemBaseType]).validate_python(response.json())
        base_type_ids = {
            base_type.baseType: base_type.itemBaseTypeId for base_type in base_types
        }
        return base_type_ids

    def set_current_hours(self, current_hours: dict[int, int]):
        for transformer in self.transformers:
            transformer.set_current_hours(current_hours)

    def set_currencies(self, currencies: dict[tuple[int, str], Currency]):
        for transformer in self.transformers:
            transformer.set_currencies(currencies)

    @sync_timing_tracker
    def transform_and_insert(
        self,
        organized_items: OrganizedItemsByCategory,
    ):
        for transformer in self.transformers:
            transformer.transform_and_insert(
                getattr(organized_items, transformer.identifier),
            )

    def end_of_hour_cleanup(self):
        self.roll_processor.log_missing_modifiers()
        for transformer in self.transformers:
            transformer.end_of_hour_cleanup()


CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class TransformerBase[RemoveSchemaType, UpdateSchemaType, CreateSchemaType](ABC):
    detector: CategoryDetectorBase
    identifier: str

    url = settings.BACKEND_BASE_URL
    sub_path: str
    url: str

    remove_subpath: str | None = None
    update_subpath: str | None = None
    insert_subpath: str | None = None

    pom_auth_headers = get_superuser_token_headers(url)

    def __init__(
        self,
        league_to_id: dict[str, int],
        item_base_types: dict[str, int],
        roll_processor: RollProcessor,
    ):
        self.identifier = self.detector.identifier
        self.url = f"{self.url}/{self.sub_path}/"

        self.type_adapters: dict[Literal["remove", "update", "insert"], TypeAdapter] = {
            "remove": TypeAdapter(list[RemoveSchemaType]),
            "update": TypeAdapter(list[UpdateSchemaType]),
            "insert": TypeAdapter(list[CreateSchemaType]),
        }

        self.league_to_id = league_to_id
        self.item_base_types = item_base_types
        self.roll_processor = roll_processor

    def set_current_hours(self, current_hours: dict[int, int]):
        self.current_hours = current_hours

    def set_currencies(self, currencies: dict[tuple[int, str], Currency]):
        self.currencies = currencies
        self.league_to_mirror = dict[int, Currency]()
        for league_id in self.league_to_id.values():
            mirror = currencies[(league_id, "mirror")]
            self.league_to_mirror[league_id] = mirror

    @abstractmethod
    def _transform_remove(
        self, removed_items: list[CacheItemWithContext], current_hours: dict[int, int]
    ) -> list[RemoveSchemaType]:
        """Transforms items into objects for removing"""

    def _remove(self, removed_items: list[RemoveSchemaType]):
        remove_url = self.url
        if self.remove_subpath is not None:
            remove_url += f"{self.remove_subpath}/"

        send_request_safe(
            "patch",
            remove_url,
            json=self.type_adapters["remove"].validate_python(removed_items),
            headers=self.pom_auth_headers,
        )

    def _extract_price(self, item: PoeItem) -> ItemPrice | None:
        league_id = self.league_to_id[item.league]

        _, currency_amount_str, currency_type_str = item.note.split()

        currency_type = self.currencies.get((league_id, currency_type_str))
        if currency_type is None:
            return None

        currency_amount = float(currency_amount_str)

        chaos_price = currency_type.valueInChaos * currency_amount
        if self._exceeds_price_threshold(league_id, chaos_price):
            return None

        return ItemPrice(
            currencyId=currency_type.currencyId, currencyAmount=currency_amount
        )

    def _exceeds_price_threshold(self, league_id: int, chaos_price: float) -> bool:
        mirror = self.league_to_mirror[league_id]
        price_in_mirrors = chaos_price / mirror.valueInChaos

        return price_in_mirrors > settings.MAX_MIRROR_PRICE

    @abstractmethod
    def _transform_update(self, changed_items: list[PoeItem]) -> list[UpdateSchemaType]:
        """Transforms items into objects for updating"""

    def _update(self, changed_items: list[UpdateSchemaType]):
        update_url = self.url
        if self.update_subpath is not None:
            update_url += f"{self.update_subpath}/"

        send_request_safe(
            "put",
            update_url,
            json=self.type_adapters["update"].dump_python(
                changed_items, exclude_none=True
            ),
            headers=self.pom_auth_headers,
        )

    @abstractmethod
    def _transform(self, new_items: list[PoeItem]) -> CreateSchemaType:
        """Transforms items, using currencies info, into a create schema for the relevant table"""

    def _insert(self, transformed: list[CreateSchemaType]):
        insert_url = self.url
        if self.insert_subpath is not None:
            insert_url += f"{self.insert_subpath}/"

        send_request_safe(
            "post",
            insert_url,
            json=self.type_adapters["insert"].dump_python(
                transformed, exclude_none=True
            ),
            headers=self.pom_auth_headers,
        )

    def transform_and_insert(self, items: OrganizedItems):
        if items.removed_items:
            transformed_remove = self._transform_remove(items.removed_items)
            self._remove(transformed_remove)

        if items.changed_items:
            transformed_update = self._transform_update(items.changed_items)
            self._update(transformed_update)

        if items.new_items:
            transformed = self._transform(items.new_items)
            self._insert(transformed)

    @abstractmethod
    def end_of_hour_cleanup(self):
        """Does necessary cleanup at the end of the hour (eg. unidentified items)"""


class UniqueTransformer(
    TransformerBase[ItemAvailabilityExpired, ItemAvailabilityUpdated, ItemCreate]
):
    detector = UniqueDetector()
    sub_path = "item"

    remove_subpath = "availability"
    update_subpath = "availability"

    def _transform_remove(
        self, removed_items: list[CacheItemWithContext]
    ) -> list[ItemAvailabilityExpired]:
        transformed = list[ItemAvailabilityExpired]()
        for item in removed_items:
            league_id = self.league_to_id[item.league]

            transformed.append(
                ItemAvailabilityExpired(
                    gameItemId=item.id,
                    leagueId=league_id,
                    validTo=self.current_hours[self.league_to_id],
                )
            )

        return transformed

    def _transform_update(
        self, changed_items: list[PoeItem]
    ) -> list[ItemAvailabilityUpdated]:
        patches = list[ItemAvailabilityUpdated]()
        for item in changed_items:
            game_item_id = item.id
            league_id = self.league_to_id[item.league]

            price = self._extract_price(item)
            if price is None:
                continue

            patches.append(
                ItemAvailabilityUpdated(
                    gameItemId=game_item_id,
                    leagueId=league_id,
                    price=price,
                    validFrom=self.current_hours[league_id],
                )
            )

        return patches

    def _transform(self, new_items: list[PoeItem]) -> ItemCreate:
        transformed = list[ItemCreate]()
        for item in new_items:
            game_item_id = item.id
            league_id = self.league_to_id[item.league]

            price = self._extract_price(item)
            if price is None:
                continue

            modifiers = self.roll_processor.extract_modifiers(item)
            if modifiers is None:
                continue

            item_base_type_id = self.item_base_types[item.base_type]

            first_observed = self.current_hours[league_id]

            item_base = ItemBase(
                game_item_id=game_item_id,
                league_id=league_id,
                item_base_type_id=item_base_type_id,
                first_observed=first_observed,
                **item.model_dump(),
            )

            transformed.append(
                ItemCreate(item=item_base, price=price, modifiers=modifiers)
            )

        return transformed

    def end_of_hour_cleanup(self):
        pass


# class UnidentifiedUniqueTransformer(TransformerBase):
#     detector = UnidentifiedUniqueDetector()
#     sub_path = "unidentified_item"
