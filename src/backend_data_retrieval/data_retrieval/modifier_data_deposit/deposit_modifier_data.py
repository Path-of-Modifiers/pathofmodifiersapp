import requests
import logging
import os
import pandas as pd
from typing import Iterator, Optional

from modifier_data_deposit.modifier_processing_modules import (
    add_regex,
    check_for_updated_text_rolls,
    check_for_updated_numerical_rolls,
    check_for_additional_modifier_types,
)
from modifier_data_deposit.utils import df_to_JSON
from pom_api_authentication import get_basic_authentication, get_super_authentication
from external_data_retrieval.config import settings

logging.basicConfig(
    filename="modifier_data_deposit.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)-8s:%(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

CASCADING_UPDATE = True


class DataDepositer:
    def __init__(self) -> None:
        self.new_data_location = "modifier_data_deposit/modifier_data"
        if "localhost" not in settings.BASEURL:
            self.url = f"https://{settings.BASEURL}"
        else:
            self.url = "http://src-backend-1"
        self.url += "/api/api_v1/modifier/"
        self.update_disabled = not CASCADING_UPDATE
        self.pom_api_authentication = get_super_authentication()

        self.modifier_types = [
            "implicit",
            "explicit",
            "delve",
            "fractured",
            "synthesized",
            "unique",
            "corrupted",
            "enchanted",
            "veiled",
        ]

        self.logger = logging.getLogger("modifier_data_deposit")

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

    def _get_current_modifiers(self) -> Optional[pd.DataFrame]:
        self.logger.info("Retrieving previously deposited data.")
        headers = {"Authorization": get_basic_authentication()}
        df = pd.read_json(self.url, dtype=str, storage_options=headers)
        if df.empty:
            self.logger.info("Found no previously deposited data.")
            return None
        else:
            self.logger.info("Successfully retrieved previously deposited data.")
            return df

    def _update_duplicates(
        self, duplicate_df: pd.DataFrame, current_modifiers_df: pd.DataFrame
    ) -> None:
        if self.update_disabled:
            return None
        self.logger.info("Checking if duplicates contain updated information.")

        current_duplicate_modifiers_df = current_modifiers_df.loc[
            current_modifiers_df["effect"].isin(duplicate_df["effect"])
        ].copy()

        # We sort them so that they line up.
        # We go through in reverse, as we wish to start with the row that has the highest position.
        current_duplicate_modifiers_df.sort_values(
            by=["effect", "position"], ascending=False, inplace=True
        )
        duplicate_df.sort_values(
            by=["effect", "position"], ascending=False, inplace=True
        )

        update_url = self.url + "?modifierId={}"

        rolls = None
        for (_, row_cur), (_, row_new) in zip(
            current_duplicate_modifiers_df.iterrows(),
            duplicate_df.iterrows(),
        ):
            put_update = False
            data = df_to_JSON(row_cur, request_method="put")
            position = int(data["position"])
            # if position is higher than 1, we want to store the types of rolls it has
            if position >= 1 and rolls is None:
                effect = data["effect"]
                same_modifier_df = duplicate_df.loc[
                    duplicate_df["effect"] == effect
                ].copy()
                rolls = []
                for _, same_modifier_row in same_modifier_df.iterrows():
                    if not pd.isna(same_modifier_row["static"]):
                        pass
                    elif not pd.isna(same_modifier_row["textRolls"]):
                        rolls.append(same_modifier_row["textRolls"])
                    else:
                        # We only need to check if the roll is of type float,
                        # which we only need 'minRoll' for and not both 'minRoll' and 'maxRoll'
                        rolls.append(same_modifier_row["minRoll"])

            if "updatedAt" in data:
                data.pop("updatedAt")

            if not pd.isna(row_new["static"]):
                pass
            elif not pd.isna(row_new["textRolls"]):
                data, put_update = check_for_updated_text_rolls(
                    data=data, row_new=row_new, rolls=rolls, logger=self.logger
                )
            else:
                data, put_update = check_for_updated_numerical_rolls(
                    data=data, row_new=row_new, rolls=rolls, logger=self.logger
                )

            data, put_update = check_for_additional_modifier_types(
                data=data,
                put_update=put_update,
                row_new=row_new,
                modifier_types=self.modifier_types,
                logger=self.logger,
            )

            if put_update:
                self.logger.info("Pushed updated modifier to the database.")
                response = requests.put(
                    update_url.format(row_cur["modifierId"]),
                    json=data,
                    headers={
                        "accept": "application/json",
                        "Content-Type": "application/json",
                    },
                    # add HTTP Basic Auth
                    auth=self.pom_api_authentication,
                )
                response.raise_for_status()

            # We reset the rolls if the position is 0, because then the next row will be a new modifier
            if position == 0 and rolls is not None:
                rolls = None

    def _remove_duplicates(self, new_modifiers_df: pd.DataFrame) -> pd.DataFrame:
        current_modifiers_df = self._get_current_modifiers()

        new_modifiers_df.drop_duplicates(inplace=True)

        if current_modifiers_df is None:
            self.logger.info("Skipping duplicate removing due to no previous data")
            return new_modifiers_df

        self.logger.info("Removing duplicate modifiers")
        duplicate_mask = new_modifiers_df["effect"].isin(current_modifiers_df["effect"])

        duplicate_df = new_modifiers_df.loc[duplicate_mask].copy()
        self._update_duplicates(duplicate_df, current_modifiers_df)
        non_duplicate_df = new_modifiers_df.loc[~duplicate_mask].copy()

        return non_duplicate_df

    def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = add_regex(df, logger=self.logger)
        df = self._remove_duplicates(df.copy(deep=True))
        return df

    def _insert_data(self, df: pd.DataFrame) -> None:
        if df.empty:
            return None
        df_json = df_to_JSON(df, request_method="post")
        self.logger.info("Inserting data into database.")
        response = requests.post(
            self.url,
            json=df_json,
            headers={"accept": "application/json", "Content-Type": "application/json"},
            auth=self.pom_api_authentication,
        )
        response.raise_for_status()

        self.logger.info("Successfully inserted data into database.")

    def deposit_data(self) -> None:
        for df in self._load_data():
            df = self._process_data(df)
            self._insert_data(df)


def main():
    data_depositer = DataDepositer()
    data_depositer.deposit_data()
    return 0


if __name__ == "__main__":
    main()
