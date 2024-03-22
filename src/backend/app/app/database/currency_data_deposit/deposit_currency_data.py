import json
import requests
import logging
import os
import pandas as pd
from typing import Dict, Iterator, List, Optional
from copy import deepcopy

from app.external_data_retrieval.transforming_data.transforming_dynamic_data.transform_poe_ninja_currency_api_data import (
    TransformPoeNinjaCurrencyAPIData,
    load_currency_data,
)


logging.basicConfig(
    filename="history.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)-8s:%(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

TESTING = True
BASEURL = "http://localhost"  # TODO update when on virtual machine
CASCADING_UPDATE = False


class CurrencyDataDepositor:
    def __init__(self, currency_data: pd.DataFrame) -> None:
        self.url = BASEURL + "/api/api_v1/currency/"
        self.currency_data: pd.DataFrame = currency_data

        self.logger = logging.getLogger(__name__)

    def _df_to_json(self, df: pd.DataFrame) -> List[Dict]:
        df_json = df.to_dict(
            "records"
        )  # Converts to a list of dicts, where each dict is a row
                      
        return df_json

    def _insert_currency_data(self, currency_dict_list: List[Dict]) -> None:
        self.logger.info("Inserting currency data into database.")

        response = requests.post(
            self.url,
            json=currency_dict_list,
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        response.raise_for_status()

        self.logger.info("Successfully inserted currency data into database.")

    def deposit_currency_data(self) -> None:
        currency_dict_list = self._df_to_json(self.currency_data)
        self._insert_currency_data(currency_dict_list)


def main():
    currency_data = load_currency_data()
    transformed_currency_data = TransformPoeNinjaCurrencyAPIData(currencies_df=currency_data).transform_into_tables()

    currency_data_depositor = CurrencyDataDepositor(transformed_currency_data)
    currency_data_depositor.deposit_currency_data()


if __name__ == "__main__":
    main()
