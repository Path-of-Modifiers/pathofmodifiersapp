import logging
import os
from collections.abc import Iterator
from typing import Literal

import pandas as pd
import requests

from external_data_retrieval.config import settings
from data_deposit.utils import df_to_JSON
from pom_api_authentication import (
    get_superuser_token_headers,
)


class DataDepositerBase:
    def __init__(
        self, data_type: Literal["modifier", "itemBaseType"], *, logger: logging.Logger
    ) -> None:
        self.logger = logger

        if "localhost" not in settings.BASEURL:
            self.base_url = f"https://{settings.BASEURL}"
        else:
            self.base_url = "http://src-backend-1"

        self.base_url += "/api/api_v1"
        self.pom_auth_headers = get_superuser_token_headers(self.base_url)

        self.data_type = data_type
        self.new_data_location = f"data_deposit/{data_type}/{data_type}_data"
        self.data_url = f"{self.base_url}/{data_type}/"

    def _load_data(self) -> Iterator[pd.DataFrame]:
        for filename in os.listdir(self.new_data_location):
            filepath = os.path.join(self.new_data_location, filename)

            self.logger.info(f"Loading new data from '{filename}'.")
            df = pd.read_csv(filepath, dtype=str, comment="#", index_col=False)
            self.logger.info("Successfully loaded new data.")
            self.logger.info("Recording attached comments:")
            with open(filepath) as infile:
                for line in infile:
                    if "#" == line[0]:
                        self.logger.info(line.rstrip())
                    else:
                        self.logger.info("End of attached comments.")
                        break

            yield df

    def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError("DataDepositerBase is not supposed to be used alone.")

    def _insert_data(self, df: pd.DataFrame) -> None:
        if df.empty:
            return None
        df_json = df_to_JSON(df, request_method="post")
        self.logger.info("Inserting data into database.")
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        headers.update(self.pom_auth_headers)
        response = requests.post(
            self.data_url,
            json=df_json,
            headers=headers,
        )
        response.raise_for_status()

        self.logger.info("Successfully inserted data into database.")

    def deposit_data(self) -> None:
        for df in self._load_data():
            df = self._process_data(df)
            self._insert_data(df)
