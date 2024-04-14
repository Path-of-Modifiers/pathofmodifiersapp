import requests
import logging
import os
import pandas as pd
from typing import Dict, List

from app.database.utils import df_to_JSON


logging.basicConfig(
    filename="history.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)-8s:%(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

BASEURL = os.getenv("DOMAIN")


class DynamicDataDepositor:
    def __init__(self, df_data: pd.DataFrame, api_v1_object: str) -> None:
        """_summary_

        Args:
            df_data (pd.DataFrame): _description_
            api_v1_object (str): _description_. For instance, "currency"
        """

        if BASEURL != "localhost":
            self.api_v1_url = "https://"
        self.api_v1_url += BASEURL + f"/api/api_v1/{api_v1_object}/"

        self.df_data: pd.DataFrame = df_data

        self.logger = logging.getLogger(__name__)

    def _insert_data(self, data_dict_list: List[Dict]) -> None:
        self.logger.info("Inserting dynamic data into database.")

        response = requests.post(
            self.url,
            json=data_dict_list,
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        response.raise_for_status()

        self.logger.info("Successfully inserted dynamic data into database.")

    def deposit_data(self) -> None:
        data_dict_list = df_to_JSON(self.df_data)
        self._insert_data(data_dict_list)
