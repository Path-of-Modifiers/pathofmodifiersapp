from typing import List, Tuple
import pandas as pd
import requests
from tqdm import tqdm


class PoeNinjaCurrencyAPIHandler:
    def __init__(self, url: str) -> None:

        self.url = url

    def _json_to_df(self, currencies: List) -> pd.DataFrame:
        df = pd.json_normalize(currencies)

        return df

    def _make_request(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Makes an initial, synchronous, API call.
        """
        response = requests.get(self.url)
        if response.status_code >= 300:
            response.raise_for_status()
        response_json = response.json()

        currencies = response_json["lines"]
        currency_details = response_json["currencyDetails"]

        return currencies, currency_details

    def store_data(self, path: str) -> None:
        """
        Stores the data in a CSV. Only to be used for testing purposes.
        """
        currencies, currency_details = self._make_request()
        df_currencies = self._json_to_df(currencies)
        df_currency_details = self._json_to_df(currency_details)

        df_currencies.to_csv(path)
        df_currency_details.to_csv(path)
