import os
import requests
import logging
from typing import Dict, List
import pandas as pd

from external_data_retrieval.data_retrieval.poe_ninja_currency_retrieval.poe_ninja_currency_api import (
    PoeNinjaCurrencyAPIHandler,
)
from modifier_data_deposit.utils import insert_data, retrieve_data

BASEURL = os.getenv("DOMAIN")


def load_currency_data():
    """
    Loads data from the poe.ninja currency API.
    """
    poe_ninja_currency_api_handler = PoeNinjaCurrencyAPIHandler(
        url="https://poe.ninja/api/data/currencyoverview?league=Necropolis&type=Currency"
    )

    currencies_df = poe_ninja_currency_api_handler.make_request()

    return currencies_df


class TransformPoeNinjaCurrencyAPIData:
    def __init__(self, logger_parent: logging.Logger):
        if "localhost" not in BASEURL:
            self.url = f"https://{BASEURL}"
        else:
            self.url = "http://src-backend-1"
        self.url += "/api/api_v1"
        self.logger = logger_parent.getChild("transform_ninja")

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
        response = requests.get(self.url + "/currency/latest_currency_id/")
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
        currency_df = self._create_currency_table(currency_df)
        currency_df = self._transform_currency_table(currency_df)
        currency_df = self._clean_currency_table(currency_df)
        insert_data(
            currency_df, url=self.url, table_name="currency", logger=self.logger
        )
        currency_id = self._get_latest_currency_id_series(currency_df)

        currency_df = currency_df.assign(currencyId=currency_id)
        return currency_df


def main():
    currency = load_currency_data()
    currency_data_transformed = TransformPoeNinjaCurrencyAPIData(currencies_df=currency)

    currency_table = currency_data_transformed.transform_into_tables()

    print(currency_table.head())

    return 0


if __name__ == "__main__":
    main()
