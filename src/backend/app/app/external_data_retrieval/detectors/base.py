import pandas as pd
from typing import Tuple


class DetectorBase:
    """
    Base class for searching stashes for items we want to store and process further
    """

    wanted_items = {}
    found_items = {}

    def __init__(self) -> None:
        """
        `self.n_unique_items_found` needs to be stored inbetween item detector sessions.
        """
        self.n_unique_items_found = 0

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

        return df

    def iterate_stashes(
        self, df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, int, int, pd.DataFrame]:
        """
        TODO
        """

        df_leftover = self._general_filter(df)
        df_filtered = self._specialized_filter(df)

        df_leftover = df_leftover.loc[df_leftover.index.isin(df_filtered.index)]

        item_count = len(df_filtered)
        self.n_unique_items_found = len(self.found_items.keys())

        return df_filtered, item_count, self.n_unique_items_found, df_leftover
