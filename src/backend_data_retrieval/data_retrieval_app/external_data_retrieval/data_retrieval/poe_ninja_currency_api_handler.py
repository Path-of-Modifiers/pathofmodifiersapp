import pandas as pd
import requests

from data_retrieval_app.logs.logger import external_data_retrieval_logger as logger


class PoENinjaCurrencyAPIHandler:
    def __init__(self, url: str) -> None:
        self.url = url

    def _combine_currency_data(self, currencies: list, currency_details: list) -> list:
        """
        Combines the currency data.
        """
        currencies_df = self._json_to_df(currencies)
        currency_details_df = self._json_to_df(currency_details)

        combined_currency_data_df = currencies_df.merge(
            currency_details_df,
            how="left",
            # left_on="pay.pay_currency_id",
            # right_on="id",
            left_on="currencyTypeName",
            right_on="name",
        )
        return combined_currency_data_df

    def _json_to_df(self, currencies: list) -> pd.DataFrame:
        df = pd.json_normalize(currencies)

        return df

    def make_request(self) -> pd.DataFrame:
        """
        Makes an initial, synchronous, API call.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except Exception as e:
            logger.error(
                f"The following error occurred while making request in poe ninja currency handler: {e}"
            )
            raise e
        response_json = response.json()

        currencies = response_json["lines"]
        currency_details = response_json["currencyDetails"]

        combined_currency_data_df = self._combine_currency_data(
            currencies, currency_details
        )

        return combined_currency_data_df

    def store_data_to_csv(self, path: str) -> None:
        """
        Stores the data in a CSV. Only to be used for testing purposes.
        """
        currencies_df = self.make_request()

        currencies_df.to_csv(path + "/poe_ninja_currencies.csv", index=False)
