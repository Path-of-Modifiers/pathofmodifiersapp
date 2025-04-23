import os
from collections.abc import Iterator
from typing import Literal

import pandas as pd
import requests

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.logs.logger import data_deposit_logger as logger
from data_retrieval_app.pom_api_authentication import (
    get_superuser_token_headers,
)
from data_retrieval_app.utils import df_to_JSON


class DataDepositorBase:
    def __init__(self, data_type: Literal["modifier", "item_base_type"]) -> None:
        if "localhost" not in settings.DOMAIN:
            self.base_url = f"https://{settings.DOMAIN}"
        else:
            self.base_url = "http://src-backend-1"

        self.base_url += "/api/api_v1"
        self.pom_auth_headers = get_superuser_token_headers(self.base_url)

        self.new_data_location = (
            f"data_retrieval_app/data_deposit/{data_type}/{data_type}_data"
        )

        data_type_parts = data_type.split("_")
        data_type = data_type_parts.pop(0)
        while data_type_parts:
            data_type += data_type_parts.pop(0).capitalize()
        self.data_type = data_type
        self.data_url = f"{self.base_url}/{data_type}/"

    def _load_data(self) -> Iterator[pd.DataFrame]:
        for filename in os.listdir(self.new_data_location):
            filepath = os.path.join(self.new_data_location, filename)

            self.logged_file_comments = {}
            logger.info(f"Loading new data from '{filename}'.")
            df = pd.read_csv(filepath, dtype=str, comment="#", index_col=False)
            logger.info("Successfully loaded new data.")
            logger.info("Recording attached comments:")
            with open(filepath) as infile:
                for line in infile:
                    if "#" == line[0]:
                        logger.info(line.rstrip())
                        split_line = line[1:].split(":")
                        self.logged_file_comments[split_line[0].strip()] = split_line[
                            1
                        ].strip()
                    else:
                        logger.info("End of attached comments.")
                        break

            yield df

    def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError("DataDepositorBase is not supposed to be used alone.")

    def _insert_data(self, df: pd.DataFrame) -> None:
        if df.empty:
            return None
        df_json = df_to_JSON(df, request_method="post")
        logger.info("Inserting data into database.")
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        headers.update(self.pom_auth_headers)
        try:
            response = requests.post(
                self.data_url,
                json=df_json,
                headers=headers,
            )
            response.raise_for_status()
        except Exception as e:
            logger.error(f"The following error occurred while inserting data: {e}")
            raise e

        logger.info("Successfully inserted data into database.")

    def deposit_data(self) -> None:
        for df in self._load_data():
            df = self._process_data(df)
            self._insert_data(df)
