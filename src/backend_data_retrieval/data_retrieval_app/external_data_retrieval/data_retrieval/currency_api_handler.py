from typing import Any

import pandas as pd

from data_retrieval_app.logs.logger import external_data_retrieval_logger as logger
from data_retrieval_app.utils import get_data_safe


class CurrencyAPIHandler:
    def __init__(self, url: str) -> None:
        self.url = url

    def _json_to_df(self, currencies: list) -> pd.DataFrame:
        df = pd.json_normalize(currencies)

        return df

    def make_request(self, leagues: list[dict[str, Any]]) -> pd.DataFrame:
        """
        Makes an initial, synchronous, API call.
        """
        df = None
        for league in leagues:
            response = get_data_safe(
                self.url.format(league=league["name"].replace(" ", "+")), logger=logger
            )
            response_json = response.json()

            items_df = pd.json_normalize(response_json["items"])
            currency_df = items_df[items_df["category"] == "currency"]
            currency_df["leagueId"] = league["leagueId"]
            if df is None:
                df = currency_df
            else:
                df = pd.concat((df, currency_df))
        return df

    def store_data_to_csv(self, path: str) -> None:
        """
        Stores the data in a CSV. Only to be used for testing purposes.
        """
        currencies_df = self.make_request()

        currencies_df.to_csv(path + "/currencies.csv", index=False)
