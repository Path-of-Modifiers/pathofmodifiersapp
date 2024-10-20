from io import StringIO

import pandas as pd
import requests

from data_retrieval_app.data_deposit.data_depositor_base import DataDepositorBase
from data_retrieval_app.data_deposit.modifier.modifier_processing_modules import (
    ModifierRegexCreator,
    check_for_additional_modifier_types,
    check_for_new_related_unique,
    check_for_updated_numerical_rolls,
    check_for_updated_text_rolls,
)
from data_retrieval_app.logs.logger import data_deposit_logger as logger
from data_retrieval_app.utils import df_to_JSON

CASCADING_UPDATE = True


class ModifierDataDepositor(DataDepositorBase):
    def __init__(self) -> None:
        super().__init__(data_type="modifier")

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
        self.regex_creator = ModifierRegexCreator()

        self.update_disabled = not CASCADING_UPDATE

    def _get_current_modifiers(self) -> pd.DataFrame:
        logger.info("Retrieving previously deposited data.")

        response = requests.get(self.data_url, headers=self.pom_auth_headers)

        df = pd.DataFrame()
        # Check if the request was successful
        if response.status_code == 200:
            # Load the JSON data into a pandas DataFrame
            json_io = StringIO(response.content.decode("utf-8"))
            df = pd.read_json(json_io, dtype=str)

        if df.empty:
            logger.info("Found no previously deposited data.")
            return None
        else:
            logger.info("Successfully retrieved previously deposited data.")
            return df

    def _update_duplicates(
        self, duplicate_df: pd.DataFrame, current_modifiers_df: pd.DataFrame
    ) -> None:
        if self.update_disabled:
            return None
        logger.info("Checking if duplicates contain updated information.")

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

        update_url = self.data_url + "?modifierId={}"

        rolls = None
        for (_, row_cur), (_, row_new) in zip(
            current_duplicate_modifiers_df.iterrows(),
            duplicate_df.iterrows(),
            strict=False,
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
                same_modifier_df.sort_values(
                    by="position", inplace=True
                )  # So that the rolls are added in the correct order
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
                    data=data,
                    row_new=row_new,
                    rolls=rolls,
                    regex_creator=self.regex_creator,
                )
            else:
                data, put_update = check_for_updated_numerical_rolls(
                    data=data, row_new=row_new
                )

            data, put_update = check_for_additional_modifier_types(
                data=data,
                put_update=put_update,
                row_new=row_new,
                modifier_types=self.modifier_types,
            )

            data, put_update = check_for_new_related_unique(
                data=data,
                put_update=put_update,
                new_related_unique=self.logged_info["Unique Name"],
            )

            if put_update:
                logger.info("Pushed updated modifier to the database.")
                headers = {
                    "accept": "application/json",
                    "Content-Type": "application/json",
                }
                headers.update(self.pom_auth_headers)
                try:
                    response = requests.put(
                        update_url.format(row_cur["modifierId"]),
                        json=data,
                        headers=headers,
                        # add HTTP Basic Auth
                    )
                    response.raise_for_status()
                except Exception as e:
                    logger.error(
                        "The following error occurred while making request:", e
                    )
                    raise e

            # We reset the rolls if the position is 0, because then the next row will be a new modifier
            if position == 0 and rolls is not None:
                rolls = None

    def _remove_duplicates(self, new_modifiers_df: pd.DataFrame) -> pd.DataFrame:
        current_modifiers_df = self._get_current_modifiers()

        new_modifiers_df = new_modifiers_df.drop_duplicates()

        if current_modifiers_df is None:
            logger.info("Skipping duplicate removing due to no previous data")
            return new_modifiers_df

        logger.info("Removing duplicate modifiers")
        duplicate_mask = new_modifiers_df["effect"].isin(current_modifiers_df["effect"])

        duplicate_df = new_modifiers_df.loc[duplicate_mask].copy()
        self._update_duplicates(duplicate_df, current_modifiers_df)
        non_duplicate_df = new_modifiers_df.loc[~duplicate_mask].copy()

        return non_duplicate_df

    def _track_comments(self, df: pd.DataFrame) -> pd.DataFrame:
        df["relatedUniques"] = self.logged_info["Unique Name"]

        return df

    def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.regex_creator.add_regex(df.copy())
        df = self._remove_duplicates(df.copy())
        df = self._track_comments(df.copy())
        return df
