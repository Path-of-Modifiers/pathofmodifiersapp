import re
import pandas as pd

from logs.logger import transform_poe_api_logger as logger

pd.set_option("display.max_colwidth", None)


class RollProcessor:
    def __init__(self, modifier_df: pd.DataFrame):
        self.modifier_df = modifier_df

        static_modifier_mask = modifier_df["static"] == "True"
        self.static_modifier_df = modifier_df.loc[static_modifier_mask]

        dynamic_modifier_df = modifier_df.loc[~static_modifier_mask]

        # sort based on length of effect
        sorted_index_mask = dynamic_modifier_df["effect"].str.len().sort_values().index
        self.dynamic_modifier_df = dynamic_modifier_df.reindex(sorted_index_mask)

    def _pre_processing(self, df: pd.DataFrame) -> pd.DataFrame:
        df.loc[:, "modifier"] = df["modifier"].replace(
            r"\\n|\n", " ", regex=True
        )  # Replaces newline with a space, so that it does not mess up the regex and matches modifiers in the `modifier` table

        return df

    def _process_static(
        self, df: pd.DataFrame, static_modifers_mask: pd.Series[bool]
    ) -> pd.DataFrame:
        """
        Static modifiers must be processed first, to reduce the amount of modifiers
        processed by the much more expensive dynamic modifier processing.
        """
        static_modifier_df = self.static_modifier_df

        static_df = df.loc[static_modifers_mask]
        static_df.loc[:, "position"] = "0"
        static_df.loc[:, "effect"] = static_df.loc[:, "modifier"]

        merged_static_df = static_df.merge(
            static_modifier_df, on=["effect", "position"], how="left"
        )
        failed_df = merged_static_df.loc[merged_static_df["static"].isna()]

        if failed_df.empty:
            logger.debug(
                f"Failed to merge static modifier with modifier in DB.\n{failed_df}"
            )
            # remove all modifiers that failed to merge
            # NOTE this should never happen
            merged_static_df = merged_static_df.loc[~merged_static_df["static"].isna()]

        return merged_static_df

    def _process_dynamic(
        self, df: pd.DataFrame, static_modifers_mask: pd.Series[bool]
    ) -> pd.DataFrame:
        """
        A much more expensive operation
        """
        dynamic_modifier_df = self.dynamic_modifier_df
        dynamic_df = df.loc[~static_modifers_mask]  # Everything not static is dynamic

        dynamic_df.loc[:, "effect"] = dynamic_df.loc[:, "modifier"]

        def extract_rolls_and_effect(matchobj: re.Match) -> str:
            effect: str = matchobj.group(0)
            rolls = matchobj.groups()
            for roll in rolls:
                effect = effect.replace(roll, "#")

            effect_and_rolls_dict = {"effect": effect, "rolls": rolls}

            return str(effect_and_rolls_dict)

        # The process must be broken down into a for-loop as the replacement is unique
        for regex in dynamic_modifier_df["regex"].unique():
            dynamic_df.loc[:, ["effect", "rolls"]] = pd.json_normalize(
                dynamic_df.loc[:, "effect"].str.replace(
                    regex, extract_rolls_and_effect, regex=True
                )
            )

        # If there are rows in the dataframe which contain empty lists, something has failed
        failed_df = dynamic_df.loc[dynamic_df["roll"].str.len() == 0]
        if failed_df.empty:
            logger.critical(
                (
                    "Failed to add rolls to listed modifiers, this likely means"
                    " the modifier is legacy or there was a new expansion."
                )
            )
            logger.critical(
                f"These items have missing modifiers: {failed_df['name'].unique().tolist()}"
            )
            logger.critical(
                f"These modifiers were not present in the database: {failed_df['effect'].unique().tolist()}"
            )
            dynamic_df = dynamic_df.loc[dynamic_df["roll"].str.len() != 0]

        # Creates a column for position, which contains a list of numerical strings
        dynamic_df.loc[:, "position"] = dynamic_df.loc[:, "roll"].apply(
            lambda x: [str(i) for i in range(len(x))]
        )

        # Each row describes one roll
        dynamic_df = dynamic_df.explode(["roll", "position"])

        merged_dynamic_df = dynamic_df.merge(
            dynamic_modifier_df, on=["effect", "position"], how="left"
        )

        # If all of these fields are still NA, it means that modifier was not matched with a modifier in our DB
        failed_df = merged_dynamic_df.loc[
            merged_dynamic_df[["minRoll", "maxRoll", "textRolls"]].isna().all(axis=1)
        ]
        if failed_df.empty:
            logger.info(
                (
                    "Some modifiers did not find their counterpart in the database."
                    " This likely means the modifier is new or has been reworded.\n"
                    f"{failed_df[['effect', 'minRoll', 'maxRoll', 'textRolls']]}"
                )
            )
            merged_dynamic_df = merged_dynamic_df.loc[
                ~merged_dynamic_df[["minRoll", "maxRoll", "textRolls"]]
                .isna()
                .all(axis=1)
            ]

        def convert_text_roll_to_index(row: pd.DataFrame) -> int:
            if row["textRolls"] != "None":
                text_rolls = row["textRolls"].split("-")
                roll = text_rolls.index(row["roll"])
            else:
                roll = row["roll"]

            return roll

        merged_dynamic_df["roll"] = merged_dynamic_df.apply(
            convert_text_roll_to_index, axis=1
        )  # The `roll` column now contains a number

        return merged_dynamic_df

    def _add_order_id(
        self, ready_static_df: pd.DataFrame, ready_dynamic_df: pd.DataFrame
    ) -> tuple[pd.DataFrame]:
        # Lets you easily identify static modifiers in the item modifier table
        ready_static_df["orderId"] = -1

        # Uses cumcount, which is similiar to range(n_duplicate_mods)
        ready_dynamic_df["orderId"] = ready_dynamic_df.groupby(
            ["itemId", "modifierId"]
        ).cumcount()

        return ready_static_df, ready_dynamic_df

    def add_rolls(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self._pre_processing(df.copy())

        static_modifers_mask = df["modifier"].isin(self.static_modifier_df["effect"])

        ready_static_df = self._process_static(df.copy(), static_modifers_mask)
        ready_dynamic_df = self._process_dynamic(df.copy(), static_modifers_mask)

        ready_static_df, ready_dynamic_df = self._add_order_id(
            ready_static_df.copy(), ready_dynamic_df.copy()
        )

        processed_df = pd.concat(
            (ready_static_df, ready_dynamic_df), axis=0, ignore_index=True
        )  # static and dynamic item modifiers are combined into one dataframe again

        processed_df.to_csv("test.csv", index=False, encoding="utf-8")
        return processed_df
