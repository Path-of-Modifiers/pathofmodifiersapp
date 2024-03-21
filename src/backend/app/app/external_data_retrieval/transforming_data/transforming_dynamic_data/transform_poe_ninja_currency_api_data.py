import json
from typing import Dict, List
import pandas as pd

from app.external_data_retrieval.data_retrieval.poe_ninja_currency_retrieval.poe_ninja_currency_api import (
    PoeNinjaCurrencyAPIHandler,
)


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
    def __init__(self, currencies_df: pd.DataFrame) -> None:
        self.currencies_df = currencies_df

    def _create_currency_table(self):
        """
        Creates the currency table.
        """
        self.currencies_df.rename(
            columns={
                "tradeId": "tradeName",
                "chaosEquivalent": "valueInChaos",
                "icon": "iconURL",
            },
            inplace=True,
        )

    def _transform_currency_table(self) -> pd.DataFrame:
        self.currencies_df["valueInChaos"][0] = 1

        self.currencies_df = self.currencies_df[
            self.currencies_df["tradeName"].notnull()
        ]

    def _clean_currency_table(self) -> pd.DataFrame:
        """
        Cleans the currency table of unnecessary columns.
        """

        self.currencies_df.drop(
            self.currencies_df.columns.difference(
                ["tradeName", "valueInChaos", "iconURL"]
            ),
            axis=1,
            inplace=True,
        )
        print(self.currencies_df)

    def transform_into_tables(self) -> pd.DataFrame:
        """
        Transforms the data into tables and transforms with help functions.
        """
        self._create_currency_table()
        self._clean_currency_table()
        self._transform_currency_table()

        return self.currencies_df


def main():
    currency = load_currency_data()
    currency_data_transformed = TransformPoeNinjaCurrencyAPIData(currencies_df=currency)

    currency_table = currency_data_transformed.transform_into_tables()

    print(currency_table.head())

    return 0


if __name__ == "__main__":
    main()
