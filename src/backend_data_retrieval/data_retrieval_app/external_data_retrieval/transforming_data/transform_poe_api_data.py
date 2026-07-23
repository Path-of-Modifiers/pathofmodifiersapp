from typing import Any

import pandas as pd
from requests.exceptions import HTTPError

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.external_data_retrieval.transforming_data.roll_processor import (
    RollProcessor,
)
from data_retrieval_app.external_data_retrieval.utils import sync_timing_tracker
from data_retrieval_app.logs.logger import transform_logger as logger
from data_retrieval_app.pom_api_authentication import get_superuser_token_headers
from data_retrieval_app.utils import get_data_safe, insert_data

pd.options.mode.chained_assignment = None  # default="warn"


class PoEAPIDataTransformerBase:
    def __init__(
        self,
        leagues: list[dict[str, Any]],
    ) -> None:
        logger.debug("Initializing PoEAPIDataTransformer")

        self.base_url = settings.BACKEND_BASE_URL
        self.pom_auth_headers = get_superuser_token_headers(self.base_url)
        self.roll_processor = RollProcessor()

        self.league_to_id = {league["name"]: league["leagueId"] for league in leagues}

        logger.debug("Initializing PoEAPIDataTransformer done.")

    def _create_item_table(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates the basis of the `item` table.
        """
        self.item_columns = [
            "itemId",
            "id",
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

        return item_df

    def _find_not_too_highly_priced_item_mask(
        self,
        currency_df: pd.DataFrame,
        item_currency_merged_df: pd.DataFrame,
    ) -> pd.Series:
        """
        Some items are too highly priced to be legitimate. A boundary of the price equivelant to
        >= 10 mirrors are seen to be too high priced.

        1. Find currency type and amount equiveland in chaos
        """

        mirror_row = currency_df.loc[currency_df["tradeName"] == "mirror"]
        mirror_value = mirror_row["valueInChaos"].get(0, 100_000)

        currency_too_high_mask = (
            item_currency_merged_df["valueInChaos"]
            * item_currency_merged_df["currencyAmount"].astype("float")
            > mirror_value * 10
        )

        return ~currency_too_high_mask

    @sync_timing_tracker
    def _transform_item_table(
        self,
        item_df: pd.DataFrame,
        currency_df: pd.DataFrame,
        item_base_types: dict[str, int],
        current_hours: dict[int, int],
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

        item_df["leagueId"] = item_df["league"].map(self.league_to_id)
        item_df["createdHoursSinceLaunch"] = item_df["leagueId"].map(current_hours)

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

        rename_map = {**rename_extended_map, "id": "gameItemId"}
        item_df = item_df.rename(columns=rename_map)

        note_series = None
        if "note" in item_df.columns:
            note_series = item_df["stash"].str.split(" ")

        stash_series = None
        if "stash" in item_df.columns:
            stash_series = item_df["stash"].str.split(" ")

        if note_series is not None:
            currency_series = note_series
            if stash_series is not None:
                currency_series = currency_series.where(
                    item_df["note"].str.contains("~"), stash_series
                )
        else:
            currency_series = stash_series

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
            left_on=["currencyType", "leagueId"],
            right_on=["tradeName", "leagueId"],
            suffixes=(None, "_y"),
        )

        price_found_mask = ~item_df["tradeName"].isna()

        self.price_found_mask = price_found_mask

        item_df = item_df.loc[self.price_found_mask]

        not_too_high_priced_item_mask = self._find_not_too_highly_priced_item_mask(
            currency_df, item_df
        )
        self.items_not_too_high_priced_mask = not_too_high_priced_item_mask

        item_df = item_df.loc[self.items_not_too_high_priced_mask]

        return item_df

    @property
    def item_table_columns_to_not_drop(self) -> set[str]:
        try:
            dont_drop_columns = self._item_table_columns_to_not_drop
        except AttributeError:
            dont_drop_columns = {
                "gameItemId",
                "name",
                "leagueId",
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
        response = get_data_safe(
            f"{self.base_url}/item/latest_item_id/",
            headers=self.pom_auth_headers,
            logger=logger,
        )
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
        current_hours: dict[int, int],
    ) -> pd.Series:
        """
        Needs to return item ids, as it is used to connect the item modifiers
        """
        item_df = self._create_item_table(df)
        item_df = self._transform_item_table(
            item_df, currency_df, item_base_types, current_hours=current_hours
        )
        item_df = self._clean_item_table(item_df)
        insert_data(
            item_df,
            url=self.base_url,
            table_name="item",
            logger=logger,
            headers=self.pom_auth_headers,
        )
        item_id = self._get_latest_item_id_series(item_df)
        logger.debug("Latest item id found: " + str(item_id))
        return item_id

    @sync_timing_tracker
    def _transform_unidentified_item_table(
        self,
        item_df: pd.DataFrame,
        currency_df: pd.DataFrame,
        item_base_types: dict[str, int],
        current_hours: dict[int, int],
    ) -> pd.DataFrame:
        """
        For convenience, all unid items are stored in divine prices
        """
        item_df = self._transform_item_table(
            item_df, currency_df, item_base_types, current_hours=current_hours
        )

        item_df["chaos_value"] = (
            item_df["currencyAmount"].astype(float) * item_df["valueInChaos"]
        )

        for league in item_df["leagueId"].unique():
            divine_row = currency_df.loc[
                (currency_df["leagueId"] == league)
                & (currency_df["tradeName"] == "divine")
            ].iloc[0]

            divine_id = divine_row["currencyId"]
            divine_value = divine_row["valueInChaos"]

            item_league_mask = item_df["leagueId"] == league
            item_df.loc[item_league_mask, "currencyId"] = divine_id
            item_df.loc[item_league_mask, "currencyAmount"] = (
                item_df.loc[item_league_mask, "chaos_value"] / divine_value
            )
        return item_df

    def _clean_unidentified_item_table(self, item_df: pd.DataFrame) -> pd.DataFrame:
        """
        Gets rid of unnecessay information, so that only fields needed for the DB remains.

        Only selects unidentified items and always drops suffixes and prefixes
        """

        dont_drop_columns = {
            "name",
            "itemBaseTypeId",
            "createdHoursSinceLaunch",
            "leagueId",
            "currencyId",
            "ilvl",
            "currencyAmount",
            "identified",
            "rarity",
        }

        item_df.drop(
            item_df.columns.difference(dont_drop_columns),
            axis=1,
            inplace=True,
            errors="ignore",
        )

        unidentified_item_df = item_df.loc[~item_df["identified"]]

        return unidentified_item_df

    def _aggregate_unidentified_item_table(
        self,
    ):
        """
        Should run once at the end of every hour. For safety, it also aggregates all previous
        hours, in case of previous unfortunate errors.
        """
        response = get_data_safe(
            f"{self.base_url}/unidentifiedItem/non_aggregated/",
            headers=self.pom_auth_headers,
            logger=logger,
        )
        unid_df = pd.DataFrame(response.json())
        if unid_df.empty:
            logger.info("Found no unidentified items to aggregate")
            return

        group_cols = [
            "leagueId",
            "name",
            "itemBaseTypeId",
            "createdHoursSinceLaunch",
            "ilvl",
            "identified",
            "currencyId",
            "rarity",
        ]

        g = unid_df.groupby(group_cols)

        unid_df["calc_avg"] = g["currencyAmount"].transform("mean")
        unid_df["calc_std"] = g["currencyAmount"].transform("std")
        unid_df["calc_count"] = g["itemId"].transform("count")

        filtered_df = unid_df[
            unid_df["currencyAmount"].between(
                unid_df["calc_avg"] - 1.97 * unid_df["calc_std"],
                unid_df["calc_avg"] + 1.97 * unid_df["calc_std"],
            )
            | unid_df["calc_std"].isna()
        ]

        result_df = filtered_df.groupby(group_cols, as_index=False).agg(
            currencyAmount=("currencyAmount", "mean"),
            nItems=("calc_count", "first"),
        )
        result_df["aggregated"] = True
        logger.info("Pushing aggregated unidentified items")
        insert_data(
            result_df,
            url=self.base_url,
            table_name="unidentifiedItem/add_aggregated",
            logger=logger,
            headers=self.pom_auth_headers,
        )

    def _process_unidentified_item_table(
        self,
        df: pd.DataFrame,
        currency_df: pd.DataFrame,
        item_base_types: dict[str, int],
        current_hours: dict[int, int],
    ) -> None:
        item_df = self._create_item_table(df)
        item_df = self._transform_unidentified_item_table(
            item_df, currency_df, item_base_types, current_hours=current_hours
        )
        item_df = self._clean_unidentified_item_table(item_df)
        insert_data(
            item_df,
            url=self.base_url,
            table_name="unidentifiedItem",
            logger=logger,
            headers=self.pom_auth_headers,
        )

    def _create_item_modifier_table(
        self, df: pd.DataFrame, *, item_id: pd.Series
    ) -> pd.DataFrame:
        """
        The `item_modifier` table heavily relies on what type of item the modifiers
        belong to.
        """
        raise NotImplementedError("Only available in child classes")

    def _transform_item_modifier_table(
        self,
        item_modifier_df: pd.DataFrame,
        current_hours: dict[int, int],
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
        current_hours: dict[int, int],
    ) -> None:
        item_modifier_df = self._create_item_modifier_table(
            df, item_id=item_id, current_hours=current_hours
        )
        item_modifier_df = self._transform_item_modifier_table(item_modifier_df)
        item_modifier_df = self._clean_item_modifier_table(item_modifier_df)
        insert_data(
            item_modifier_df,
            url=self.base_url,
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
        current_hours: dict[int, int],
    ) -> None:
        self.roll_processor.add_modifier_df(modifier_df)
        try:
            logger.debug("Transforming data into tables.")
            logger.debug("Processing data tables.")
            item_id = self._process_item_table(
                df.copy(deep=True),
                currency_df=currency_df,
                item_base_types=item_base_types,
                current_hours=current_hours,
            )
            self._process_unidentified_item_table(
                df.copy(deep=True),
                currency_df=currency_df,
                item_base_types=item_base_types,
                current_hours=current_hours,
            )
            self._process_item_modifier_table(
                df.copy(deep=True),
                item_id=item_id,
                current_hours=current_hours,
            )
            logger.debug("Successfully transformed data into tables.")

        except HTTPError as e:
            logger.exception(f"Something went wrong:\n{repr(e)}")
            raise e

    def end_of_hour_cleanup(self):
        self._aggregate_unidentified_item_table()


class UniquePoEAPIDataTransformer(PoEAPIDataTransformerBase):
    @sync_timing_tracker
    def _create_item_modifier_table(
        self,
        df: pd.DataFrame,
        *,
        item_id: pd.Series,
        current_hours: dict[int, int],
    ) -> pd.DataFrame:
        """
        A similiar process to creating the item table, only this time the
        relevant column contains a list and not a JSON-object
        """
        item_modifier_columns = ["name", "explicitMods", "league"]
        item_modifier_df = df.loc[
            self.price_found_mask,
            item_modifier_columns,
        ]

        item_modifier_df = item_modifier_df.loc[
            self.items_not_too_high_priced_mask
        ].reset_index()

        item_modifier_df["itemId"] = item_id
        item_modifier_df["leagueId"] = item_modifier_df["league"].map(self.league_to_id)
        item_modifier_df["createdHoursSinceLaunch"] = item_modifier_df["leagueId"].map(
            current_hours
        )
        item_modifier_df = item_modifier_df.explode("explicitMods", ignore_index=True)

        item_modifier_df.rename({"explicitMods": "modifier"}, axis=1, inplace=True)

        return item_modifier_df

    @sync_timing_tracker
    def _transform_item_modifier_table(
        self,
        item_modifier_df: pd.DataFrame,
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
                "position",
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
