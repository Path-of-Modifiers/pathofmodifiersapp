import pandas as pd


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
        Filtering away items that are never usefull
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

        return df

    def iterate_stashes(self, df: pd.DataFrame) -> tuple:
        """
        Goes through all stashes searching for items that correspond to `self.wanted_items`.
        `self.n_unique_items_found` is calculated by the number of keys in `self.found_items`.
        The `_check_item` method, which is unique to item categories, is defined in a child class.

        Parameters:
            :param stashes: (list) A list of stash objects as defined by GGG.
            :return: (tuple) Wanted stashes, how many new items was found, number of different items that have been found so far, stashes that still need to be filtered.
        """

        df_potential = self._general_filter(df)
        df_filtered = self._specialized_filter(df)

        df_leftover = df_potential.loc[df_potential.index.isin(df_filtered.index)]

        item_count = len(df_filtered)
        self.n_unique_items_found = len(self.found_items.keys())

        return df_filtered, item_count, self.n_unique_items_found, df_leftover
