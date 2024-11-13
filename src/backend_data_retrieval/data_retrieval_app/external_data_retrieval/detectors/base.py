import pandas as pd

from data_retrieval_app.external_data_retrieval.config import settings


class DetectorBase:
    """
    Base class for searching stashes for items we want to store and process further
    """

    wanted_items = {}
    found_items = {}

    current_league = settings.CURRENT_SOFTCORE_LEAGUE

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
        if "stash" in columns or "note" in columns:
            if "stash" in columns and "note" in columns:
                df = df.loc[df["stash"].str.startswith("~") | df["note"].notna()]
            elif "stash" in columns:
                df = df.loc[df["stash"].str.startswith("~")]
            else:
                df = df.loc[df["note"].notna()]
        else:
            return pd.DataFrame(columns=df.columns)

        df = df.loc[df["league"] == self.current_league]

        return df

    def _specialized_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError(
            "This method is implemented in child classes. Do not use the base on its own."
        )

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

        item_count = len(df_filtered)
        self.n_unique_items_found = len(self.found_items.keys())

        return df_filtered, item_count, self.n_unique_items_found, df_leftover
