import json
from typing import Dict, List
import pandas as pd

from app.external_data_retrieval.data_retrieval.poe_ninja_currency_retrieval.poe_ninja_currency_api import (
    PoeNinjaCurrencyAPIHandler,
)


def load_data():
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

    def _create_currency_table(self) -> pd.DataFrame:
        """
        Creates the currency table.
        """
        currency_table = self.currencies_df.copy()
        currency_table = currency_table.rename(
            columns={
                "tradeId": "tradeName",
                "chaosEquivalent": "valueInChaos",
                "icon": "iconURL",
            }
        )

        return currency_table

    def _clean_currency_table(self) -> pd.DataFrame:

        self.currencies_df.drop(
            self.currencies_df.columns.difference(
                ["tradeName", "valueInChaos", "iconURL"]
            ),
            axis=1,
            inplace=True,
        )

    def clean_currency_details_table(self) -> pd.DataFrame:
        """
        Cleans the currency details data.
        """
        currency_details_df = self.currency_details_df.copy()

        currency_details_df["icon"] = currency_details_df["icon"].apply(
            lambda x: x.split("?")[0]
        )
        currency_details_df["icon"] = currency_details_df["icon"].apply(
            lambda x: x.replace(
                "https://web.poecdn.com/image/Art/2DItems/Currency/", ""
            )
        )

        return currency_details_df
