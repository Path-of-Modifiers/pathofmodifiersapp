import pandas as pd
import requests
from requests.exceptions import HTTPError

from data_deposit.utils import insert_data
from external_data_retrieval.config import settings
from external_data_retrieval.transforming_data.utils import (
    get_rolls,
)
from logs.logger import transform_logger as logger
from pom_api_authentication import get_superuser_token_headers

pd.options.mode.chained_assignment = None  # default="warn"


class PoeAPIDataTransformer:
    def __init__(self):
        logger.debug("Initializing PoeAPIDataTransformer")
        if "localhost" not in settings.BASEURL:
            self.url = f"https://{settings.BASEURL}"
        else:
            self.url = "http://src-backend-1"
        self.url += "/api/api_v1"
        logger.debug("Url set to: " + self.url)

        self.pom_auth_headers = get_superuser_token_headers(self.url)
        logger.debug("Headers set to: " + str(self.pom_auth_headers))
        logger.debug("Initializing PoeAPIDataTransformer done.")

    def _create_account_table(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates the basis of the `account` table.
        It is not immediately processed in order to save compute power later.
        """
        self.account_columns = ["accountName"]
        account_df = df.loc[:, self.account_columns]

        return account_df

    def _clean_account_table(self, account_df: pd.DataFrame) -> pd.DataFrame:
        account_df.drop_duplicates(inplace=True)

        return account_df

    def _transform_account_table(self, account_df: pd.DataFrame) -> pd.DataFrame:
        account_df.drop_duplicates("accountName", inplace=True)

        account_df["isBanned"] = None

        return account_df

    def _process_account_table(self, df: pd.DataFrame) -> None:
        account_df = self._create_account_table(df)
        account_df = self._transform_account_table(account_df)
        insert_data(
            account_df,
            url=self.url,
            table_name="account",
            logger=logger,
            on_duplicate_pkey_do_nothing=True,
            headers=self.pom_auth_headers,
        )

    def _create_stash_table(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates the basis of the `stash` table.
        It is not immediately processed in order to save compute power later.
        """
        self.stash_columns = ["stashId", "accountName", "public", "league"]
        stash_df = df.loc[:, self.stash_columns]

        return stash_df

    def _clean_stash_table(self, stash_df: pd.DataFrame) -> pd.DataFrame:
        stash_df = stash_df.drop_duplicates(["stashId"])

        return stash_df

    def _process_stash_table(self, df: pd.DataFrame) -> None:
        stash_df = self._create_stash_table(df)
        stash_df = self._clean_stash_table(stash_df)
        insert_data(
            stash_df,
            url=self.url,
            table_name="stash",
            logger=logger,
            on_duplicate_pkey_do_nothing=True,
            headers=self.pom_auth_headers,
        )

    def _create_item_table(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates the basis of the `item` table, using parts of `stash` table.

        The `item` table requires the `stashId` as a foreign key. This is
        why the `stash` table was not immediately processed.
        """
        self.item_columns = [
            "itemId",
            "gameItemId",
            "stashId",
            "name",
            "icon",
            "league",
            "typeLine",
            "baseType",
            "rarity",
            "identified",
            "ilvl",
            "note",
            "forum_note",
            "corrupted",
            "delve",
            "fractured",
            "synthesized",
            "replica",
            "elder",
            "shaper",
            "influences.shaper",
            "influences.elder",
            "influences.crusader",
            "influences.hunter",
            "influences.redeemer",
            "influences.warlord",
            "searing",
            "tangled",
            "foilVariation",
            "stash",
        ]
        item_df = df.loc[
            :, [column for column in self.item_columns if column in df.columns]
        ]  # Can't guarantee all columns are present
        return item_df

    def _transform_item_table(
        self, item_df: pd.DataFrame, currency_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        The `item` table requires a foreign key to the `currency` table.
        Everything related to the price of the item is stored in the `node`
        attribute.

        There are two types of listings in POE, exact price and asking price which are
        represented by `price` and `b/o` respectively.
        """

        def get_currency_amount(element):
            if isinstance(element, list):
                if len(element) == 3:
                    return element[1] if element[0] in ["~b/o", "~price"] else pd.NA

            return pd.NA

        def get_currency_type(element):
            if isinstance(element, list):
                if len(element) == 3:
                    return element[2] if element[0] in ["~b/o", "~price"] else ""

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

        influence_columns = [
            column for column in item_df.columns if "influences" in column
        ]
        item_df["influences"] = item_df.apply(
            lambda row: transform_influences(row, influence_columns), axis=1
        )

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
            currency_df, how="left", left_on="currencyType", right_on="tradeName"
        )

        return item_df

    def _clean_item_table(self, item_df: pd.DataFrame) -> pd.DataFrame:
        """
        Gets rid of unnecessay information, so that only fields needed for the DB remains.
        """
        drop_list = [
            "influences.shaper",
            "influences.elder",
            "influences.crusader",
            "influences.hunter",
            "influences.redeemer",
            "influences.warlord",
            "stash",
            "currencyType",
            "tradeName",
            "valueInChaos",
            "itemId",
            "createdAt",
            "iconUrl",
        ]
        item_df.drop(
            drop_list,
            axis=1,
            inplace=True,
            errors="ignore",
        )

        item_df.rename({"icon": "iconUrl"}, axis=1, inplace=True)
        return item_df

    def _get_latest_item_id_series(self, item_df: pd.DataFrame) -> pd.Series:
        response = requests.get(
            self.url + "/item/latest_item_id/", headers=self.pom_auth_headers
        )
        response.raise_for_status()
        latest_item_id = int(response.text)

        item_id = pd.Series(
            range(latest_item_id - len(item_df) + 1, latest_item_id + 1), dtype=int
        )

        return item_id

    def _process_item_table(
        self, df: pd.DataFrame, currency_df: pd.DataFrame
    ) -> pd.Series:
        item_df = self._create_item_table(df)
        item_df = self._transform_item_table(item_df, currency_df)
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
        self, df: pd.DataFrame, *, item_id: pd.Series, modifier_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        The `item_modifier` table heavily relies on what type of item the modifiers
        belong to.
        """
        raise NotImplementedError("Only available in child classes")

    def _transform_item_modifier_table(
        self, item_modifier_df: pd.DataFrame, *, modifier_df: pd.DataFrame
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
        self, df: pd.DataFrame, modifier_df: pd.DataFrame, item_id: pd.Series
    ) -> None:
        item_modifier_df = self._create_item_modifier_table(
            df, item_id=item_id, modifier_df=modifier_df
        )

        item_modifier_df = self._transform_item_modifier_table(
            item_modifier_df, modifier_df
        )

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
    ) -> None:
        try:
            logger.debug("Transforming data into tables.")
            logger.debug("Processing data tables.")
            self._process_account_table(df.copy(deep=True))
            self._process_stash_table(df.copy(deep=True))
            item_id = self._process_item_table(
                df.copy(deep=True), currency_df=currency_df
            )
            self._process_item_modifier_table(
                df.copy(deep=True), item_id=item_id, modifier_df=modifier_df
            )
            logger.debug("Successfully transformed data into tables.")

        except HTTPError as e:
            logger.exception(f"Something went wrong:\n{repr(e)}")
            raise e


class UniquePoeAPIDataTransformer(PoeAPIDataTransformer):
    def _create_item_modifier_table(
        self, df: pd.DataFrame, *, item_id: pd.Series, modifier_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        A similiar process to creating the item table, only this time the
        relevant column contains a list and not a JSON-object
        """
        self.item_modifier_columns = ["name", "explicitMods"]

        item_modifier_df = df.loc[:, self.item_modifier_columns].reset_index()

        item_modifier_df["itemId"] = item_id
        item_modifier_df = item_modifier_df.explode("explicitMods", ignore_index=True)

        item_modifier_df.rename({"explicitMods": "modifier"}, axis=1, inplace=True)

        return item_modifier_df

    def _transform_item_modifier_table(
        self, item_modifier_df: pd.DataFrame, modifier_df: pd.DataFrame
    ) -> pd.DataFrame:
        item_modifier_df = get_rolls(df=item_modifier_df, modifier_df=modifier_df)

        return item_modifier_df

    def _clean_item_modifier_table(self, item_modifer_df: pd.DataFrame):
        """
        Gets rid of unnecessay information, so that only fields needed for the DB remains.
        """
        item_modifer_df.drop(
            item_modifer_df.columns.difference(
                ["itemId", "modifierId", "orderId", "position", "roll"]
            ),
            axis=1,
            inplace=True,
        )
        return item_modifer_df
