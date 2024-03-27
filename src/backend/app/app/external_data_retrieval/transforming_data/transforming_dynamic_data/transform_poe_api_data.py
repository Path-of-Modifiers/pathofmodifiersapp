import os
import requests
import pandas as pd
from typing import List

from app.database.utils import df_to_JSON
from app.external_data_retrieval.transforming_data.transforming_dynamic_data.utils import (
    get_rolls,
)


BASEURL = os.getenv("DOMAIN")


class PoeAPIDataTransformer:
    def __init__(self):
        self.url = BASEURL + "/api/api_v1"

    def _preprocessing(self, df: pd.DataFrame) -> pd.DataFrame:
        response = requests.get(self.url + "/item/latest_item_id/")
        response.raise_for_status()
        n_items_in_db = int(response.text)

        df = df.reset_index()
        df["itemId"] = df.index + n_items_in_db

        return df

    def _post_table(self, df: pd.DataFrame, table_name: str) -> None:
        data = df_to_JSON(df, request_method="post")
        requests.post(self.url + f"/{table_name}/", json=data)

    def _create_account_table(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates the basis of the `account` table.
        It is not immediately processed in order to save compute power later.
        """
        self.account_columns = ["accountName"]
        account_df = df.loc[:, self.account_columns]

        return account_df

    def _transform_account_table(self, account_df: pd.DataFrame) -> pd.DataFrame:
        account_df.drop_duplicates("accountName")

        account_df["isBanned"] = None

        return account_df

    def _clean_account_table(self, account_df: pd.DataFrame) -> pd.DataFrame:

        db_account_df = pd.read_json(self.url + "/account/", dtype=str)
        if db_account_df.empty:
            return account_df

        account_df = account_df.loc[
            ~account_df["accountName"].isin(db_account_df["accountName"])
        ]

        return account_df

    def _process_account_table(self, df: pd.DataFrame) -> None:
        account_df = self._create_account_table(df)
        account_df = self._transform_account_table(account_df)
        account_df = self._clean_account_table(account_df)
        self._post_table(account_df, table_name="account")

    def _create_stash_table(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates the basis of the `stash` table.
        It is not immediately processed in order to save compute power later.
        """
        self.stash_columns = ["stashId", "accountName", "public", "league"]
        stash_df = df.loc[:, self.stash_columns]

        return stash_df

    def _clean_stash_table(self, stash_df: pd.DataFrame) -> pd.DataFrame:
        stash_df = stash_df.drop_duplicates(["stashId", "accountName", "league"])

        return stash_df

    def _process_stash_table(self, df: pd.DataFrame) -> None:
        stash_df = self._create_stash_table(df)
        stash_df = self._clean_stash_table(stash_df)
        self._post_table(stash_df, table_name="stash")

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
        ]
        item_df = df.loc[
            :, [column for column in self.item_columns if column in df.columns]
        ]  # Can't guarantee all columns are present

        return item_df

    def _transform_item_table(self, item_df: pd.DataFrame) -> pd.DataFrame:
        """
        The `item` table requires a foreign key to the `currency` table.
        Everything related to the price of the item is stored in the `node`
        attribute.

        There are two types of listings in POE, exact price and asking price which are
        represented by `price` and `b/o` respectively.
        """
        currency_series = item_df["note"].str.split(" ")
        influence_columns = [
            column for column in item_df.columns if "influences" in column
        ]

        def get_currency_amount(element):
            if isinstance(element, list):
                return element[1] if element[0] in ["~b/o", "~price"] else pd.NA
            else:
                return pd.NA

        def get_currency_type(element):
            if isinstance(element, list):
                return element[2] if element[0] in ["~b/o", "~price"] else ""
            else:
                return ""

        def transform_influences(row: pd.DataFrame, influence_columns: List[str]):
            if not row[influence_columns].any():
                return pd.NA
            else:
                influence_dict = {}
                for influence_column in influence_columns:
                    if row[influence_column]:
                        influence_dict[influence_column.replace("influences.", "")] = (
                            True
                        )
                return influence_dict

        item_df["influences"] = item_df.apply(
            lambda row: transform_influences(row, influence_columns), axis=1
        )

        item_df["currencyAmount"] = currency_series.apply(get_currency_amount)
        item_df["currencyType"] = currency_series.apply(get_currency_type)

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
            "sockets",
            "socketedItems",
            "lockedToAccount",
            "lockedToCharacter",
            "duplicated",
            "split",
            "unmodifiable",
            "cisRaceReward",
            "seaRaceReward",
            "thRaceReward",
            "properties",
            "noteableProperties",
            "additionalProperties",
            "nextLevelRequirements",
            "talismanTier",
            "rewards",
            "secDescrText",
            "utilityMods",
            "logbookMods",
            "enchantMods",
            "scourgeMods",
            "ultimatumMods",
            "explicitMods",
            "craftedMods",
            "fracturedMods",
            "crucibleMods",
            "cosmeticMods",
            "veiledMods",
            "veiled",
            "flavourTextParsed",
            "flavourTextNote",
            "prophecyText",
            "isRelic",
            "foreseeing",
            "artFilename",
            "inventoryId",
            "socket",
            "colour",
            "incubatedItem.name",
            "incubatedItem.level",
            "incubatedItem.progress",
            "incubatedItem.total",
            "scourged.tier",
            "scourged.level",
            "scourged.progress",
            "scourged.total",
            "crucible.layout",
            "crucible.nodes",
            "crucible.nodes.stats",
            "crucible.nodes.skill",
            "crucible.nodes.tier",
            "crucible.nodes.icon",
            "crucible.nodes.allocated",
            "crucible.nodes.isNoteable",
            "crucible.nodes.orbit",
            "crucible.nodes.orbitIndex",
            "crucible.nodes.out",
            "crucible.nodes.in",
            "crucible.nodes.reminderText",
            "crucible.nodes.isReward",
            "hybrid.isVaalGem",
            "hybrid.baseTypeName",
            "hybrid.properties",
            "hybrid.explicitMods",
            "hybrid.secDescrText",
            "extended.prefixes",
            "extended.suffixes",
            "descrText",
            "flavourText",
            "frameType",
            "x",
            "y",
            "requirements",
            "ruthless",
        ]
        item_df.drop(
            drop_list,
            axis=1,
            inplace=True,
            errors="ignore",
        )
        return item_df

    def _process_item_table(self, df: pd.DataFrame) -> None:
        item_df = self._create_item_table(df)
        item_df = self._transform_item_table(item_df)
        item_df = self._clean_item_table(item_df)
        self._post_table(item_df, table_name="item")

    def _create_item_modifier_table(
        self, df: pd.DataFrame, modifier_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        The `item_modifier` table heavily relies on what type of item the modifiers
        belong to.
        """
        raise NotImplementedError("Only available in child classes")

    def _transform_item_modifier_table(
        self, item_modifier_df: pd.DataFrame, modifier_df: pd.DataFrame
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
        self, df: pd.DataFrame, modifier_df: pd.DataFrame
    ) -> None:
        item_modifier_df = self._create_item_modifier_table(df, modifier_df)
        item_modifier_df = self._transform_item_modifier_table(
            item_modifier_df, modifier_df
        )
        item_modifier_df = self._clean_item_modifier_table(item_modifier_df)
        self._post_table(item_modifier_df, table_name="itemModifier")

    def transform_into_tables(
        self, df: pd.DataFrame, modifier_df: pd.DataFrame
    ) -> None:
        df = self._preprocessing(df)
        self._process_account_table(df.copy(deep=True))
        self._process_stash_table(df.copy(deep=True))
        self._process_item_table(df.copy(deep=True))
        self._process_item_modifier_table(df.copy(deep=True), modifier_df=modifier_df)


class UniquePoeAPIDataTransformer(PoeAPIDataTransformer):
    def _create_item_modifier_table(
        self, df: pd.DataFrame, modifier_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        A similiar process to creating the item table, only this time the
        relevant column contains a list and not a JSON-object
        """
        self.item_modifier_columns = ["name", "explicitMods", "itemId"]

        item_modifier_df = df.loc[:, self.item_modifier_columns]

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
        # print(item_modifer_df)
        # quit()
        return item_modifer_df
