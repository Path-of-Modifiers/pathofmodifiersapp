import json
import requests
import logging
import os
import pandas as pd
from typing import Dict, Iterator, List, Optional
from copy import deepcopy

from app.external_data_retrieval.transforming_data.transforming_dynamic_data.transform_poe_ninja_currency_api_data import (
    TransformPoeNinjaCurrencyAPIData,
    load_df_data,
)
from app.database.utils import df_to_JSON


logging.basicConfig(
    filename="history.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)-8s:%(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

TESTING = os.getenv("TESTING")
BASEURL = os.getenv("DOMAIN")
CASCADING_UPDATE = False


class DynamicDataDepositor:
    def __init__(self, df_data: pd.DataFrame, api_v1_object: str) -> None:
        """_summary_

        Args:
            df_data (pd.DataFrame): _description_
            api_v1_object (str): _description_. For instance, "currency"
        """
        self.api_v1_url = BASEURL + f"/api/api_v1/{api_v1_object}/"
        self.df_data: pd.DataFrame = df_data

        self.logger = logging.getLogger(__name__)

    def _insert_data(self, data_dict_list: List[Dict]) -> None:
        self.logger.info("Inserting currency data into database.")

        response = requests.post(
            self.url,
            json=data_dict_list,
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        response.raise_for_status()

        self.logger.info("Successfully inserted currency data into database.")

    def deposit_data(self) -> None:
        data_dict_list = df_to_JSON(self.df_data)
        self._insert_data(data_dict_list)
