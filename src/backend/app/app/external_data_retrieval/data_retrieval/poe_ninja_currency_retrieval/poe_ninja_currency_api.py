from typing import List, Tuple
import pandas as pd
import requests


class PoeNinjaCurrencyAPIHandler:
    def __init__(self, url: str) -> None:

        self.url = url

    def _combine_currency_data(self, currencies: List, currency_details: List) -> List:
        """
        Combines the currency data.
        """
        combined_currency_data = []
        for currency, currency_detail in zip(currencies, currency_details):
            combined_currency_data.append({**currency, **currency_detail})

        return combined_currency_data

    def _json_to_df(self, currencies: List) -> pd.DataFrame:
        df = pd.json_normalize(currencies)

        return df

    def make_request(self) -> pd.DataFrame:
        """
        Makes an initial, synchronous, API call.
        """
        response = requests.get(self.url)
        if response.status_code >= 300:
            response.raise_for_status()
        response_json = response.json()

        currencies = response_json["lines"]
        currency_details = response_json["currencyDetails"]

        combined_currency_data = self._combine_currency_data(
            currencies, currency_details
        )

        combined_currency_data_df = self._json_to_df(combined_currency_data)

        return combined_currency_data_df

    def store_data(self, path: str) -> None:
        """
        Stores the data in a CSV. Only to be used for testing purposes.
        """
        currencies, currency_details = self._make_request()
        df_currencies = self._json_to_df(currencies)
        df_currency_details = self._json_to_df(currency_details)

        df_currencies.to_csv(path + "/poe_ninja_currencies.csv", index=False)
        df_currency_details.to_csv(
            path + "/poe_ninja_currency_details.csv", index=False
        )


PoeNinjaCurrencyAPIHandler(
    url="https://poe.ninja/api/data/currencyoverview?league=Standard&type=Currency"
).store_data("./app/external_data_retrieval/depricated_data/test_data")
