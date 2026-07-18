from io import StringIO

import pandas as pd
import requests

from data_retrieval_app.data_deposit.data_depositor_base import DataDepositorBase
from data_retrieval_app.logs.logger import data_deposit_logger as logger
from data_retrieval_app.utils import get_data_safe


class ItemBaseTypeDataDepositor(DataDepositorBase):
    def __init__(self) -> None:
        super().__init__(data_type="item_base_type")

        self.update_url = str(self.data_url)
        self.data_url += "?on_duplicate_pkey_do_nothing=true"
        self.current_basetypes_df = self._get_current_base_types()

    def _get_current_base_types(self) -> pd.DataFrame:
        logger.info("Retrieving previously deposited data.")

        response = get_data_safe(
            self.data_url, headers=self.pom_auth_headers, logger=logger
        )

        json_io = StringIO(response.content.decode("utf-8"))
        df = pd.read_json(json_io, dtype=str)

        if df.empty:
            logger.info("Found no previously deposited data.")
            return pd.DataFrame(
                columns=[
                    "itemBaseTypeId",
                    "baseType",
                    "category",
                    "subCategory",
                    "relatedUniques",
                ]
            )
        else:
            logger.info("Successfully retrieved previously deposited data.")
            return df

    def _update_duplicates(self, duplicate_df: pd.DataFrame):
        """
        Note that this method does not remove uniques which are not present in the file.
        """
        changed_rows = duplicate_df[
            (duplicate_df["relatedUniques"] != duplicate_df["relatedUniques_y"])
            & (~duplicate_df["relatedUniques"].isna())
        ].copy()

        if not changed_rows.empty:
            logger.info(
                "Found changes in related uniques for some item base types. Updating these changes."
            )
            changed_rows["new_related_uniques"] = changed_rows.apply(
                lambda row: (
                    "|".join(
                        set(
                            row["relatedUniques"].split("|")
                            + row["relatedUniques_y"].split("|")
                        )
                    )
                    if row["relatedUniques_y"]
                    else row["relatedUniques"]
                ),
                axis=1,
            )
            headers = {
                "accept": "application/json",
                "Content-Type": "application/json",
            }
            headers.update(self.pom_auth_headers)

            for _, row in changed_rows.iterrows():
                item_base_type_id = row["itemBaseTypeId"]
                data = {
                    "baseType": row["baseType"],
                    "category": row["category"],
                    "subCategory": row["subCategory"],
                    "relatedUniques": row["new_related_uniques"],
                }

                try:
                    response = requests.put(
                        self.update_url + str(item_base_type_id),
                        json=data,
                        headers=headers,
                        # add HTTP Basic Auth
                    )
                    response.raise_for_status()
                except Exception as e:
                    logger.error(
                        f"The following error occurred while making request during _update_duplicates item base types: {e}"
                    )
                    raise e

    def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        merged_df = pd.merge(
            df,
            self.current_basetypes_df,
            how="left",
            on="baseType",
            suffixes=("", "_y"),
        )
        non_duplicate_mask = merged_df["itemBaseTypeId"].isna()
        non_duplicate_df = merged_df[non_duplicate_mask]
        non_duplicate_df = non_duplicate_df.drop(
            columns=[
                column for column in non_duplicate_df.columns if column.endswith("_y")
            ]
        )

        self._update_duplicates(merged_df[~non_duplicate_mask])

        return non_duplicate_df
