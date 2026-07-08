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
            data = {"leagueId": league_id, "name": duplicate_league_row["name"]}
            do_update = False

            old_valid_to = duplicate_league_row["validTo_y"]
            new_valid_to = duplicate_league_row["validTo"]
            data["validTo"] = new_valid_to
            if old_valid_to != new_valid_to:
                do_update = True

            old_valid_from = duplicate_league_row["validFrom_y"]
            new_valid_from = duplicate_league_row["validFrom"]
            data["validFrom"] = new_valid_from
            if old_valid_from != new_valid_from:
                do_update = True

            if do_update:
                headers = {
                    "accept": "application/json",
                    "Content-Type": "application/json",
                }
                headers.update(self.pom_auth_headers)
                try:
                    response = requests.put(
                        self.update_url + str(league_id),
                        json=data,
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
            suffixes=("", "_y"),
        )
        non_duplicate_mask = merged_df["leagueId"].isna()
        non_duplicate_df = merged_df[non_duplicate_mask]
        non_duplicate_df = non_duplicate_df.drop(
            columns=[
                column for column in non_duplicate_df.columns if column.endswith("_y")
            ]
        )

        self._update_duplicates(merged_df[~non_duplicate_mask])

        return non_duplicate_df
