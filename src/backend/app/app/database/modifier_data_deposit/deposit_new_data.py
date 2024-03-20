import requests
import logging
import os
import pandas as pd
from typing import Iterator

from app.database.modifier_data_deposit.processing_modules import add_regex
from app.database.modifier_data_deposit.utils import remove_empty_fields

logging.basicConfig(
    filename="history.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)-8s:%(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
TESTING = True
BASEURL = "http://localhost"  # TODO update when on virtual machine


class DataDepositer:
    def __init__(self) -> None:
        self.new_data_location = "new_data"

        self.logger = logging.getLogger(__name__)

    def _load_new_data(self) -> Iterator[pd.DataFrame]:
        for filename in os.listdir(self.new_data_location):
            filepath = os.path.join(self.new_data_location, filename)

            self.logger.info(f"Loading new data from '{filename}'.")
            df = pd.read_csv(filepath, dtype=str, comment="#")
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

    def _process_new_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = add_regex(df, logger=self.logger)
        return df

    def _insert_data(self, df: pd.DataFrame) -> None:
        df = df.fillna("")
        df_json = df.to_dict("records")
        df_json = remove_empty_fields(df_json)

        self.logger.info("Inserting data into database.")
        response = requests.post(
            BASEURL + "/api/api_v1/modifier/",
            json=df_json,
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        response.raise_for_status()

        self.logger.info("Successfully inserted data into database.")

    def _delete_processed_data(self):
        for filename in os.listdir(self.new_data_location):
            filepath = os.path.join(self.new_data_location, filename)
            self.logger.info(f"Deleting '{filename}'")
            if TESTING:
                os.rename(filepath, filepath.replace("new_data", "deposited_data"))
            # os.remove(filepath)
            self.logger.info(f"Deleted '{filename}'")

    def deposit_data(self) -> None:
        for df in self._load_new_data():
            df = self._process_new_data(df)
            self._insert_data(df)

        self._delete_processed_data()


def main():
    test = DataDepositer()
    test.deposit_data()
    return 0


main()
