import inspect
import time

import pandas as pd

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.logs.logger import data_retrieval_logger as logger


class DetectorBase:
    """
    Base class for searching stashes for items we want to store and process further
    """

    wanted_items = {}
    found_items = {}

    def __init__(self, enable_pbar: bool = False) -> None:
        """
        `self.n_unique_items_found` needs to be stored inbetween item detector sessions.
        """
        self.n_unique_items_found = 0

        self.prev_item_hashes_found = {}

        self.leagues = [
            settings.CURRENT_SOFTCORE_LEAGUE,
            f"Hardcore {settings.CURRENT_SOFTCORE_LEAGUE}",
        ]

        self.pbar_enabled = enable_pbar

    def _general_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filtering away items that are never useful
        """
        columns = df.columns
        if "ruthless" in columns:
            df = df.loc[df["ruthless"].isnull()]
        if "lockedToCharacter" in columns:
            df = df.loc[df["lockedToCharacter"].isnull()]
        if "lockedToAccount" in columns:
            df = df.loc[df["lockedToAccount"].isnull()]
        if "logbookMods" in columns:
            df = df.loc[df["logbookMods"].isnull()]
        if "crucible" in columns:
            df = df.loc[df["crucible"].isnull()]
        if "scourged" in columns:
            df = df.loc[df["scourged"].isnull()]
        if "hybrid" in columns:
            df = df.loc[df["hybrid"].isnull()]
        if "ultimatumMods" in columns:
            df = df.loc[df["ultimatumMods"].isnull()]
        if "stash" in columns or "note" in columns:
            if "stash" in columns and "note" in columns:
                df = df.loc[
                    df["stash"].str.startswith(("~b/o", "~price"))
                    | df["note"].str.startswith(("~b/o", "~price"))
                ]
            elif "stash" in columns:
                df = df.loc[df["stash"].str.startswith(("~b/o", "~price"))]
            else:
                df = df.loc[df["note"].str.startswith(("~b/o", "~price"))]
        else:
            return pd.DataFrame(columns=df.columns)

        df = df.loc[df["league"].isin(self.leagues)]

        return df

    def _specialized_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError(
            "This method is implemented in child classes. Do not use the base on its own."
        )

    def _filter_on_game_item_id(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        The same item can be picked up by the api, without any changes being made to the listing/item,
        because the user listed/changed another item in the same tab. We do not want to store these,
        as they pain the wrong picture of the market.

        To make sure that only updated items are kept, we also add the note, which contains the price.
        Please note that this does not consider relisting of entire tab.

        However, as of right now, these identifiers reset every ~hour. In the future we may pull
        the most recent listings from the database instead of resetting.
        """
        n_items_before_filter = len(df)

        df = df.drop_duplicates(["id", "note"])

        game_item_id = df["id"].apply(int, base=16)
        note = df["note"].apply(hash)

        hashes: pd.Series[int] = game_item_id + note

        unique_hashes = set(hashes)

        if not self.prev_item_hashes_found:
            self.prev_item_hashes_found = unique_hashes
        else:
            duplicate_hashes = self.prev_item_hashes_found.intersection(unique_hashes)
            self.prev_item_hashes_found |= unique_hashes

            items_to_drop_mask = ~hashes.isin(duplicate_hashes)
            df = df.loc[items_to_drop_mask]

        n_items_filtered = n_items_before_filter - len(df)

        logger.info(
            f'detector="{self}" {n_items_before_filter=} {n_items_filtered=} percent_of_total={1 - n_items_filtered / max(1, n_items_before_filter):.2%}'
        )

        return df

    def _snapshot(self, df: pd.DataFrame, filepath: str = None) -> None:
        """
        A method for creating a snapshot for a given dataframe. If no filepath is given, it saves the class
        this directory with the name `snapshot_{name_of_class}_{time}.csv`
        """
        if filepath is None:
            filepath = (
                inspect.getfile(DetectorBase)[:-7]
                + f"snapshot_{self}_{time.time():.0f}.csv"
            )

        logger.info(f"Saving a snapshot, for the detector {self}")
        df.to_csv(filepath, encoding="utf-8")

    def iterate_stashes(
        self, df: pd.DataFrame
    ) -> tuple[pd.DataFrame, int, int, pd.DataFrame]:
        """
        TODO
        """

        df = self._general_filter(df)
        if df.empty:
            return df, 0, self.n_unique_items_found, df
        df_filtered = self._specialized_filter(df)
        df_leftover = df.loc[~df.index.isin(df_filtered.index)]

        df_filtered = self._filter_on_game_item_id(df_filtered)

        item_count = len(df_filtered)
        if self.pbar_enabled:
            self.n_unique_items_found = len(self.found_items.keys())

        return df_filtered, item_count, self.n_unique_items_found, df_leftover
