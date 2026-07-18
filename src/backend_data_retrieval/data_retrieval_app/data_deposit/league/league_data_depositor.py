from io import StringIO

import pandas as pd
import requests

from data_retrieval_app.data_deposit.data_depositor_base import DataDepositorBase
from data_retrieval_app.logs.logger import data_deposit_logger as logger
from data_retrieval_app.utils import get_data_safe


class LeagueDataDepositor(DataDepositorBase):
    def __init__(self) -> None:
        super().__init__(data_type="league")

        self.update_url = str(self.data_url)
        self.data_url += "?on_duplicate_pkey_do_nothing=true"
        self.current_league_df = self._get_current_leagues()

    def _get_current_leagues(self) -> pd.DataFrame:
        logger.info("Retrieving previously deposited data.")

        response = get_data_safe(
            self.data_url, headers=self.pom_auth_headers, logger=logger
        )

        json_io = StringIO(response.content.decode("utf-8"))
        df = pd.read_json(json_io, dtype=str)

        if df.empty:
            logger.info("Found no previously deposited data.")
            return pd.DataFrame(columns=["name", "leagueId", "validTo", "validFrom"])
        else:
            logger.info("Successfully retrieved previously deposited data.")
            return df

    def _update_duplicates(self, duplicate_df: pd.DataFrame):
        for _, duplicate_league_row in duplicate_df.iterrows():
            league_id = int(duplicate_league_row["leagueId"])

            old_df = duplicate_league_row[
                [col for col in duplicate_league_row.index if not col.endswith("_y")]
            ]
            old_df.index = old_df.index.str.removesuffix("_x")
            old = old_df.to_dict()
            new_df = duplicate_league_row[
                [col for col in duplicate_league_row.index if not col.endswith("_x")]
            ]
            new_df.index = new_df.index.str.removesuffix("_y")
            new = new_df.to_dict()

            do_update = False
            for key, old_val in old.items():
                if new[key] != old_val:
                    do_update = True
                    break

            if do_update:
                headers = {
                    "accept": "application/json",
                    "Content-Type": "application/json",
                }
                headers.update(self.pom_auth_headers)
                try:
                    response = requests.put(
                        self.update_url + str(league_id),
                        json=new,
                        headers=headers,
                        # add HTTP Basic Auth
                    )
                    response.raise_for_status()
                except Exception as e:
                    logger.error(
                        f"The following error occurred while making request during _update_duplicates league: {e}"
                    )
                    raise e

    def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        hardcore_df = df.copy()
        hardcore_df["name"] = "Hardcore " + hardcore_df["name"]
        df = pd.concat((df, hardcore_df), ignore_index=True)
        merged_df = pd.merge(
            df,
            self.current_league_df,
            how="left",
            on="name",
            suffixes=("_x", "_y"),
        )
        non_duplicate_mask = merged_df["leagueId"].isna()
        non_duplicate_df = merged_df[non_duplicate_mask]
        non_duplicate_df = non_duplicate_df.drop(
            columns=[
                column for column in non_duplicate_df.columns if column.endswith("_y")
            ]
        )
        non_duplicate_df.columns = non_duplicate_df.columns.str.removesuffix("_x")

        self._update_duplicates(merged_df[~non_duplicate_mask])

        return non_duplicate_df
