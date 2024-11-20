import pandas as pd
import requests
from requests.exceptions import HTTPError

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.external_data_retrieval.transforming_data.roll_processor import (
    RollProcessor,
)
from data_retrieval_app.external_data_retrieval.utils import sync_timing_tracker
from data_retrieval_app.logs.logger import transform_logger as logger
from data_retrieval_app.pom_api_authentication import get_superuser_token_headers
from data_retrieval_app.utils import find_hours_since_launch, insert_data

pd.options.mode.chained_assignment = None  # default="warn"


class PoEAPIDataTransformerBase:
    def __init__(self) -> None:
        logger.debug("Initializing PoEAPIDataTransformer")
        if "localhost" not in settings.DOMAIN:
            self.url = f"https://{settings.DOMAIN}"
        else:
            self.url = "http://src-backend-1"
        self.url += "/api/api_v1"
        logger.debug("Url set to: " + self.url)

        self.pom_auth_headers = get_superuser_token_headers(self.url)
        logger.debug("Headers set to: " + str(self.pom_auth_headers))
        logger.debug("Initializing PoEAPIDataTransformer done.")

        self.roll_processor = RollProcessor()

    def _create_item_table(
        self, df: pd.DataFrame, hours_since_launch: int
    ) -> pd.DataFrame:
        """
        Creates the basis of the `item` table.
        """
        self.item_columns = [
            "itemId",
            "name",
            "league",
            "baseType",
            "typeLine",
            "ilvl",
            "rarity",
            "identified",
            "note",
            "corrupted",
            "delve",
            "fractured",
            "synthesised",
            "replica",
            "influences.shaper",
            "influences.elder",
            "influences.crusader",
            "influences.hunter",
            "influences.redeemer",
            "influences.warlord",
            "extended.prefixes",
            "extended.suffixes",
            "searing",
            "tangled",
            "foilVariation",
            "isRelic",
            "stash",
        ]
        item_df = df.loc[
            :, [column for column in self.item_columns if column in df.columns]
        ]  # Can't guarantee all columns are present

        item_df["createdHoursSinceLaunch"] = hours_since_launch
        return item_df

    @sync_timing_tracker
    def _transform_item_table(
        self,
        item_df: pd.DataFrame,
        currency_df: pd.DataFrame,
        item_base_types: dict[str, int],
    ) -> pd.DataFrame:
        """
        The `item` table requires a foreign key to the `currency` table.
        Everything related to the price of the item is stored in the `note`
        attribute.

        There are two types of listings in PoE, exact price and asking price which are
        represented by `price` and `b/o` respectively.
        """

        def transform_base_types(element):
            return item_base_types[element]

        def get_currency_amount(element):
            if len(element) == 3:
                return element[1]
            return pd.NA

        def get_currency_type(element):
            if len(element) == 3:
                return element[2]
            return ""

        def transform_influences(row: pd.DataFrame, influence_columns: list[str]):
            if not row[influence_columns].any():
                return pd.NA
            else:
                influence_dict = {}
                for influence_column in influence_columns:
                    if row[influence_column]:
                        influence_dict[
                            influence_column.replace("influences.", "")
                        ] = True
                return influence_dict

        base_type_series = item_df["baseType"]
        item_df["itemBaseTypeId"] = base_type_series.apply(transform_base_types)

        influence_columns = [
            column for column in item_df.columns if "influences" in column
        ]
        item_df["influences"] = item_df.apply(
            lambda row: transform_influences(row, influence_columns), axis=1
        )

        rename_extended_map = {}
        if "extended.prefixes" in item_df.columns:
            rename_extended_map["extended.prefixes"] = "prefixes"
        if "extended.suffixes" in item_df.columns:
            rename_extended_map["extended.suffixes"] = "suffixes"

        if rename_extended_map:
            item_df = item_df.rename(columns=rename_extended_map)

        stash_series = item_df["stash"].str.split(" ")
        currency_series = item_df["note"].str.split(" ")

        currency_series = currency_series.where(
            item_df["note"].str.contains("~"), stash_series
        )

        item_df["currencyAmount"] = currency_series.apply(get_currency_amount)
        item_df["currencyType"] = currency_series.apply(get_currency_type)

        invalid_amount_mask = ~item_df["currencyAmount"].str.match(
            r"^(([0-9]*[.])?[0-9]+)$", na=False
        )
        item_df.loc[invalid_amount_mask, "currencyAmount"] = pd.NA
        item_df.loc[invalid_amount_mask, "currencyType"] = ""

        item_df = item_df.merge(
            currency_df,
            how="left",
            left_on="currencyType",
            right_on="tradeName",
            suffixes=(None, "_y"),
        )

        self.price_found_mask = ~item_df["tradeName"].isna()

        item_df = item_df.loc[self.price_found_mask]

        return item_df

    @property
    def item_table_columns_to_not_drop(self) -> set[str]:
        try:
            dont_drop_columns = self._item_table_columns_to_not_drop
        except AttributeError:
            dont_drop_columns = {
                "name",
                "league",
                "itemBaseTypeId",
                "ilvl",
                "rarity",
                "identified",
                "currencyAmount",
                "currencyId",
                "corrupted",
                "delve",
                "fractured",
                "synthesised",
                "replica",
                "influences",
                "searing",
                "tangled",
                "prefixes",
                "suffixes",
                "foilVariation",
                "createdHoursSinceLaunch",
            }
            self._item_table_columns_to_not_drop = dont_drop_columns
        return dont_drop_columns

    @item_table_columns_to_not_drop.setter
    def item_table_columns_to_not_drop(self, columns_to_not_drop: set[str]) -> set[str]:
        self._item_table_columns_to_not_drop = columns_to_not_drop

    def _update_item_table_columns_to_not_drop(self, *, dont_drop: set[str]) -> None:
        columns_to_not_drop = self.item_table_columns_to_not_drop

        self.item_table_columns_to_not_drop = columns_to_not_drop | dont_drop

    def _clean_item_table(self, item_df: pd.DataFrame) -> pd.DataFrame:
        """
        Gets rid of unnecessay information, so that only fields needed for the DB remains.
        """

        dont_drop_columns = self.item_table_columns_to_not_drop

        item_df.drop(
            item_df.columns.difference(dont_drop_columns),
            axis=1,
            inplace=True,
            errors="ignore",
        )

        return item_df

    def _get_latest_item_id_series(self, item_df: pd.DataFrame) -> pd.Series:
        try:
            response = requests.get(
                self.url + "/item/latest_item_id/", headers=self.pom_auth_headers
            )
            response.raise_for_status()
        except Exception as e:
            logger.error("The following error occurred while making request:", e)
            raise e
        latest_item_id = int(response.text)

        item_id = pd.Series(
            range(latest_item_id - len(item_df) + 1, latest_item_id + 1), dtype=int
        )

        return item_id

    def _process_item_table(
        self,
        df: pd.DataFrame,
        currency_df: pd.DataFrame,
        item_base_types: dict[str, int],
        hours_since_launch: int,
    ) -> pd.Series:
        item_df = self._create_item_table(df, hours_since_launch=hours_since_launch)
        item_df = self._transform_item_table(item_df, currency_df, item_base_types)
        item_df = self._clean_item_table(item_df)
        insert_data(
            item_df,
            url=self.url,
            table_name="item",
            logger=logger,
            headers=self.pom_auth_headers,
        )
        item_id = self._get_latest_item_id_series(item_df)
        logger.debug("Latest item id found: " + str(item_id))
        return item_id

    def _create_item_modifier_table(
        self, df: pd.DataFrame, *, item_id: pd.Series, hours_since_launch: int
    ) -> pd.DataFrame:
        """
        The `item_modifier` table heavily relies on what type of item the modifiers
        belong to.
        """
        raise NotImplementedError("Only available in child classes")

    def _transform_item_modifier_table(
        self,
        item_modifier_df: pd.DataFrame,
        hours_since_launch: int,
    ) -> pd.DataFrame:
        """
        The `item_modifier` table heavily relies on what type of item the modifiers
        belong to.
        """
        raise NotImplementedError("Only available in child classes")

    def _clean_item_modifier_table(
        self, item_modifier_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        The `item_modifier` table heavily relies on what type of item the modifiers
        belong to.

        Gets rid of unnecessay information, so that only fields needed for the DB remains.
        """
        raise NotImplementedError("Only available in child classes")

    def _process_item_modifier_table(
        self,
        df: pd.DataFrame,
        item_id: pd.Series,
        hours_since_launch: int,
    ) -> None:
        item_modifier_df = self._create_item_modifier_table(
            df, item_id=item_id, hours_since_launch=hours_since_launch
        )
        item_modifier_df = self._transform_item_modifier_table(item_modifier_df)
        item_modifier_df = self._clean_item_modifier_table(item_modifier_df)

        insert_data(
            item_modifier_df,
            url=self.url,
            table_name="itemModifier",
            logger=logger,
            headers=self.pom_auth_headers,
        )

    def transform_into_tables(
        self,
        df: pd.DataFrame,
        modifier_df: pd.DataFrame,
        currency_df: pd.DataFrame,
        item_base_types: dict[str, int],
    ) -> None:
        self.roll_processor.add_modifier_df(modifier_df)
        try:
            logger.debug("Transforming data into tables.")
            logger.debug("Processing data tables.")
            hours_since_launch = find_hours_since_launch()
            item_id = self._process_item_table(
                df.copy(deep=True),
                currency_df=currency_df,
                item_base_types=item_base_types,
                hours_since_launch=hours_since_launch,
            )
            self._process_item_modifier_table(
                df.copy(deep=True),
                item_id=item_id,
                hours_since_launch=hours_since_launch,
            )
            logger.debug("Successfully transformed data into tables.")

        except HTTPError as e:
            logger.exception(f"Something went wrong:\n{repr(e)}")
            raise e


class UniquePoEAPIDataTransformer(PoEAPIDataTransformerBase):
    @sync_timing_tracker
    def _create_item_modifier_table(
        self, df: pd.DataFrame, *, item_id: pd.Series, hours_since_launch: int
    ) -> pd.DataFrame:
        """
        A similiar process to creating the item table, only this time the
        relevant column contains a list and not a JSON-object
        """
        item_modifier_columns = ["name", "explicitMods"]

        item_modifier_df = df.loc[
            self.price_found_mask, item_modifier_columns
        ].reset_index()

        item_modifier_df["itemId"] = item_id
        item_modifier_df = item_modifier_df.explode("explicitMods", ignore_index=True)

        item_modifier_df.rename({"explicitMods": "modifier"}, axis=1, inplace=True)

        item_modifier_df["createdHoursSinceLaunch"] = hours_since_launch

        return item_modifier_df

    @sync_timing_tracker
    def _transform_item_modifier_table(
        self, item_modifier_df: pd.DataFrame
    ) -> pd.DataFrame:
        item_modifier_df = self.roll_processor.add_rolls(df=item_modifier_df)
        return item_modifier_df

    @property
    def item_modifier_table_columns_to_not_drop(self) -> set[str]:
        try:
            dont_drop_columns = self._item_modifier_table_columns_to_not_drop
        except AttributeError:
            dont_drop_columns = {
                "itemId",
                "modifierId",
                "roll",
                "createdHoursSinceLaunch",
            }
            self._item_modifier_table_columns_to_not_drop = dont_drop_columns
        return dont_drop_columns

    @item_modifier_table_columns_to_not_drop.setter
    def item_modifier_table_columns_to_not_drop(
        self, columns_to_not_drop: set[str]
    ) -> set[str]:
        self._item_modifier_table_columns_to_not_drop = columns_to_not_drop

    def _update_item_modifier_table_columns_to_not_drop(
        self, *, dont_drop: set[str]
    ) -> None:
        columns_to_not_drop = self.item_modifier_table_columns_to_not_drop
        self.item_modifier_table_columns_to_not_drop = columns_to_not_drop | dont_drop

    def _clean_item_modifier_table(
        self, item_modifier_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Gets rid of unnecessay information, so that only fields needed for the DB remains.
        """
        dont_drop_columns = self.item_modifier_table_columns_to_not_drop

        item_modifier_df.drop(
            item_modifier_df.columns.difference(dont_drop_columns),
            axis=1,
            inplace=True,
        )

        return item_modifier_df
