import pandas as pd
import requests

from data_deposit.utils import insert_data
from external_data_retrieval.config import settings
from external_data_retrieval.data_retrieval.poe_ninja_currency_retrieval.poe_ninja_currency_api import (
    PoeNinjaCurrencyAPIHandler,
)
from logs.logger import transform_logger as logger
from pom_api_authentication import get_superuser_token_headers


def load_currency_data():
    """
    Loads data from the poe.ninja currency API.
    """
    poe_ninja_currency_api_handler = PoeNinjaCurrencyAPIHandler(
        url=f"https://poe.ninja/api/data/currencyoverview?league={settings.CURRENT_SOFTCORE_LEAGUE}&type=Currency"
    )

    currencies_df = poe_ninja_currency_api_handler.make_request()

    return currencies_df


class TransformPoeNinjaCurrencyAPIData:
    def __init__(self):
        logger.debug("Initializing TransformPoeNinjaCurrencyAPIData.")
        if "localhost" not in settings.BASEURL:
            self.url = f"https://{settings.BASEURL}"
        else:
            self.url = "http://src-backend-1"
        self.url += "/api/api_v1"
        logger.debug("Url set to: " + self.url)
        self.pom_api_headers = get_superuser_token_headers(self.url)
        logger.debug("Headers set to: " + str(self.pom_api_headers))
        logger.debug("Initializing TransformPoeNinjaCurrencyAPIData done.")

    def _create_currency_table(self, currency_df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates the currency table.
        """
        currency_df.rename(
            columns={
                "tradeId": "tradeName",
                "chaosEquivalent": "valueInChaos",
                "icon": "iconUrl",
            },
            inplace=True,
        )
        return currency_df

    def _transform_currency_table(self, currency_df: pd.DataFrame) -> pd.DataFrame:
        """
        Since a chaos orb is always worth one chaos orb, ninja does not include it in its price api.
        """
        chaos_dict = {
            "tradeName": ["chaos"],
            "valueInChaos": [1],
            "iconUrl": [
                "https://web.poecdn.com/gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvQ3VycmVuY3lSZXJvbGxSYXJlIiwidyI6MSwiaCI6MSwic2NhbGUiOjF9XQ/d119a0d734/CurrencyRerollRare.png"
            ],
        }
        chaos_df = pd.DataFrame.from_dict(chaos_dict)
        currency_df = pd.concat((currency_df, chaos_df), ignore_index=True)
        return currency_df

    def _clean_currency_table(self, currency_df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans the currency table of unnecessary columns.
        """

        currency_df.drop(
            currency_df.columns.difference(["tradeName", "valueInChaos", "iconUrl"]),
            axis=1,
            inplace=True,
        )
        currency_df = currency_df.loc[~currency_df["tradeName"].isna()].reset_index()
        return currency_df

    def _get_latest_currency_id_series(self, currency_df: pd.DataFrame) -> pd.Series:
        response = requests.get(
            self.url + "/currency/latest_currency_id/", headers=self.pom_api_headers
        )
        response.raise_for_status()
        latest_currency_id = int(response.text)

        currency_id = pd.Series(
            range(latest_currency_id - len(currency_df) + 1, latest_currency_id + 1),
            dtype=int,
        )
        return currency_id

    def transform_into_tables(self, currency_df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the data into tables and transforms with help functions.
        """
        logger.debug("Transforming data into tables.")
        currency_df = self._create_currency_table(currency_df)
        currency_df = self._transform_currency_table(currency_df)
        logger.debug("Successfully transformed data into tables.")

        logger.debug("Cleaning currency table data.")
        currency_df = self._clean_currency_table(currency_df)
        logger.debug("Successfully cleaned currency table data.")

        logger.debug("Inserting currency data into database.")
        insert_data(
            currency_df,
            url=self.url,
            table_name="currency",
            logger=logger,
            headers=self.pom_api_headers,
        )
        logger.debug("Successfully inserted currency data into database.")

        currency_id = self._get_latest_currency_id_series(currency_df)
        logger.debug("Latest currency id found: " + str(currency_id))

        currency_df = currency_df.assign(currencyId=currency_id)
        logger.debug("Successfully transformed data into tables.")
        return currency_df
