from abc import ABC, abstractmethod
from typing import Literal, TypeVar

from backend_api.app.core.schemas.currency import Currency
from backend_api.app.core.schemas.item import (
    ItemAvailabilityExpired,
    ItemAvailabilityUpdated,
    ItemBase,
    ItemCreate,
    ItemPrice,
)
from backend_api.app.core.schemas.league import League
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
from data_retrieval_app.utils import (
    get_grouped_modifiers_by_unique,
    get_item_base_type_id_by_name,
    send_request_safe,
)


class PoEAPIDataTransformer:
    url = settings.BACKEND_BASE_URL
    pom_auth_headers = get_superuser_token_headers(url)

    def __init__(
        self,
        leagues: list[League],
    ) -> None:
        logger.debug("Initializing PoEAPIDataTransformer")

        modifiers = get_grouped_modifiers_by_unique(self.pom_auth_headers)
        self.roll_processor = RollProcessor(modifiers)

        self.item_base_types = get_item_base_type_id_by_name(self.pom_auth_headers)

        self.league_to_id = {league.name: league.leagueId for league in leagues}

        logger.debug("Initializing PoEAPIDataTransformer done.")

        self.transformers: list[TransformerBase] = [
            UniqueTransformer(self),
            # UnidentifiedUniqueTransformer(self.league_to_id, item_base_types, self.roll_processor),
        ]

        self.current_hours = None
        self.currencies = None
        self.league_to_mirror = None

    def set_current_hours(self, current_hours: dict[int, int]):
        self.current_hours = current_hours

    def set_currencies(self, currencies: dict[tuple[int, str], Currency]):
        self.currencies = currencies

        self.league_to_mirror = dict[int, Currency]()
        for league_id in self.league_to_id.values():
            mirror = currencies[(league_id, "mirror")]
            self.league_to_mirror[league_id] = mirror

    def extract_valid_price(self, item: PoeItem) -> ItemPrice | None:
        if self.currencies is None:
            raise RuntimeError("Must set currencies first")

        league_id = self.league_to_id[item.league]

        _, currency_amount_str, currency_type_str = item.note.split(maxsplit=2)

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

    @sync_timing_tracker
    def transform_and_insert(
        self,
        organized_items: OrganizedItemsByCategory,
    ):
        """
        Includes inplace population of the `dismissed_items` field for each category
        Params:
            :Organized items: (OrganizedItemsByCategory) items are transformed, and inserted into the database.
                                Items which could not be tranformed are inserted into the respective `dismissed_items`
                                field.
        """
        if self.currencies is None:
            raise RuntimeError("Must set currencies first")
        if self.current_hours is None:
            raise RuntimeError("Must set current hours first")

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

    base_url = settings.BACKEND_BASE_URL
    sub_path: str

    remove_subpath: str | None = None
    update_subpath: str | None = None
    insert_subpath: str | None = None

    pom_auth_headers = get_superuser_token_headers(base_url)

    def __init__(
        self,
        main_transformer: PoEAPIDataTransformer,
    ):
        self.main_transformer = main_transformer

        self.identifier = self.detector.identifier
        self.url = f"{self.base_url}/{self.sub_path}/"

        self.type_adapters: dict[Literal["remove", "update", "insert"], TypeAdapter] = {
            "remove": TypeAdapter(list[RemoveSchemaType]),
            "update": TypeAdapter(list[UpdateSchemaType]),
            "insert": TypeAdapter(list[CreateSchemaType]),
        }

    @abstractmethod
    def _transform_remove(
        self, removed_items: list[CacheItemWithContext]
    ) -> list[RemoveSchemaType]:
        """Transforms items into objects for removing"""

    def _remove(self, removed_items: list[RemoveSchemaType]):
        remove_url = self.url
        if self.remove_subpath is not None:
            remove_url += f"{self.remove_subpath}/"

        send_request_safe(
            "patch",
            remove_url,
            json=self.type_adapters["remove"].dump_python(removed_items),
            headers=self.pom_auth_headers,
        )

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
    def _transform_new(self, new_items: list[PoeItem]) -> list[CreateSchemaType]:
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
            transformed = self._transform_new(items.new_items)
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
            league_id = self.main_transformer.league_to_id[item.league]

            transformed.append(
                ItemAvailabilityExpired(
                    gameItemId=item.id,
                    leagueId=league_id,
                    validTo=self.main_transformer.current_hours[league_id] + 1,
                )
            )

        return transformed

    def _transform_update(
        self, changed_items: list[PoeItem]
    ) -> list[ItemAvailabilityUpdated]:
        patches = list[ItemAvailabilityUpdated]()
        for item in changed_items:
            game_item_id = item.id
            league_id = self.main_transformer.league_to_id[item.league]

            price = self.main_transformer.extract_valid_price(item)
            if price is None:
                raise ValueError("An item with invalid price made it past filtering")

            patches.append(
                ItemAvailabilityUpdated(
                    gameItemId=game_item_id,
                    leagueId=league_id,
                    price=price,
                    validFrom=self.main_transformer.current_hours[league_id],
                )
            )

        return patches

    def _transform_new(self, new_items: list[PoeItem]) -> list[ItemCreate]:
        transformed = list[ItemCreate]()
        for item in new_items:
            game_item_id = item.id
            league_id = self.main_transformer.league_to_id[item.league]

            price = self.main_transformer.extract_valid_price(item)
            if price is None:
                raise ValueError("An item with invalid price made it past filtering")

            modifiers = self.main_transformer.roll_processor.extract_modifiers(item)

            item_base_type_id = self.main_transformer.item_base_types[item.base_type]

            first_observed = self.main_transformer.current_hours[league_id]

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
