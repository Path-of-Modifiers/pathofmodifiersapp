import os
import requests
import logging
from typing import Dict, List
import pandas as pd

from app.external_data_retrieval.data_retrieval.poe_ninja_currency_retrieval.poe_ninja_currency_api import (
    PoeNinjaCurrencyAPIHandler,
)
from app.database.utils import insert_data, retrieve_data

BASEURL = os.getenv("DOMAIN")


def load_currency_data():
    """
    Loads data from the poe.ninja currency API.
    """
    poe_ninja_currency_api_handler = PoeNinjaCurrencyAPIHandler(
        url="https://poe.ninja/api/data/currencyoverview?league=Affliction&type=Currency"
    )

    currencies_df = poe_ninja_currency_api_handler.make_request()

    return currencies_df


class TransformPoeNinjaCurrencyAPIData:
    def __init__(self, main_logger: logging.Logger):
        if BASEURL != "localhost":
            self.url = "https://"
        self.url += BASEURL + "/api/api_v1"
        self.logger = main_logger.getChild("transform_ninja")

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
        currency_df.loc[0, "valueInChaos"] = 1

        currency_df = currency_df[currency_df["tradeName"].notnull()]
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
        return currency_df

    def _get_latest_item_id_series(self, currency_df: pd.DataFrame) -> pd.Series:
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
        currency_df = self._clean_currency_table(currency_df)
        currency_df = self._transform_currency_table(currency_df)
        insert_data(currency_df, url=self.url, table_name="currency")
        currency_id = self._get_latest_item_id_series(currency_df)

        currency_df["currencyId"] = currency_id

        return currency_df


def main():
    currency = load_currency_data()
    currency_data_transformed = TransformPoeNinjaCurrencyAPIData(currencies_df=currency)

    currency_table = currency_data_transformed.transform_into_tables()

    print(currency_table.head())

    return 0


if __name__ == "__main__":
    main()
