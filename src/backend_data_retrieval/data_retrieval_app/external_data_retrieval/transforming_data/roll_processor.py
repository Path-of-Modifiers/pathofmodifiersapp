import re

import pandas as pd

from data_retrieval_app.logs.logger import transform_logger as logger

pd.set_option("display.max_colwidth", None)


class RollProcessor:
    @property
    def modifier_df(self) -> pd.DataFrame:
        return self._modifier_df

    @modifier_df.setter
    def modifier_df(self, modifier_df: pd.DataFrame):
        self._modifier_df = modifier_df.drop(["createdAt"], axis=1)

        static_modifier_mask = self._modifier_df["static"] == "True"
        self.static_modifier_df = self._modifier_df.loc[static_modifier_mask]

        self.dynamic_modifier_df = self._modifier_df.loc[~static_modifier_mask]

    def add_modifier_df(self, modifier_df: pd.DataFrame):
        try:
            modifier_df = self.modifier_df
        except AttributeError:
            self.modifier_df = modifier_df

    def _pre_processing(self, df: pd.DataFrame) -> pd.DataFrame:
        df.loc[:, "modifier"] = df[
            "modifier"
        ].replace(
            r"\\n|\n", " ", regex=True
        )  # Replaces newline with a space, so that it does not mess up the regex and matches modifiers in the `modifier` table

        return df

    def _process_static(
        self, df: pd.DataFrame, static_modifers_mask: pd.Series
    ) -> pd.DataFrame:
        """
        Static modifiers must be processed first, to reduce the amount of modifiers
        processed by the much more expensive dynamic modifier processing.
        """
        static_modifier_df = self.static_modifier_df

        static_df = df.loc[static_modifers_mask]
        if static_df.empty:
            return pd.DataFrame(
                columns=static_df.columns.append(static_modifier_df.columns)
            )
        static_df.loc[:, "position"] = "0"
        static_df.loc[:, "effect"] = static_df.loc[:, "modifier"]

        merged_static_df = static_df.merge(
            static_modifier_df, on=["effect", "position"], how="left"
        )
        failed_df = merged_static_df.loc[merged_static_df["static"].isna()]

        if not failed_df.empty:
            logger.debug(
                f"Failed to merge static modifier with modifier in DB.\n{failed_df}"
            )
            # remove all modifiers that failed to merge
            # NOTE this should never happen
            merged_static_df = merged_static_df.loc[~merged_static_df["static"].isna()]

        return merged_static_df

    def _get_rolls(self, dynamic_df: pd.DataFrame) -> pd.DataFrame:
        """
        Uses regex matching groups to extract the rolls and adds
        the correct effect.
        """

        def extract_rolls(matchobj: re.Match) -> str:
            rolls = [
                roll
                for roll in matchobj.groups()
                if roll not in ["reduced", "increased"]  # because of alternate spelling
            ]

            return "matched" + ":-:".join(rolls)

        dynamic_modifier_df = self.dynamic_modifier_df

        # The process must be broken down into a for-loop as the replacement is unique

        dynamic_w_rolls_df = dynamic_df.copy()
        for effect, regex in dynamic_modifier_df[["effect", "regex"]].itertuples(
            index=False
        ):
            matched_modifiers = dynamic_df["modifier"].str.replace(
                regex, extract_rolls, regex=True
            )
            matched_modifiers_mask = matched_modifiers.str.contains("matched", na=False)

            dynamic_w_rolls_df.loc[matched_modifiers_mask, "effect"] = effect
            dynamic_w_rolls_df.loc[
                matched_modifiers_mask, "roll"
            ] = matched_modifiers.loc[matched_modifiers_mask]

            dynamic_df.loc[matched_modifiers_mask, "modifier"] = pd.NA

        dynamic_w_rolls_df.loc[:, "roll"] = (
            dynamic_w_rolls_df["roll"].str.removeprefix("matched").str.split(":-:")
        )
        del dynamic_df
        dynamic_df = dynamic_w_rolls_df

        # If there are rows in the dataframe which contain empty lists, something has failed
        failed_df = dynamic_df.loc[dynamic_df["roll"].isna()]
        if not failed_df.empty:
            logger.critical(
                "Failed to add rolls to listed modifiers, this likely means"
                " the modifier is legacy or there was a new expansion."
            )
            logger.critical(
                f"These items have missing modifiers: {failed_df['name'].unique().tolist()}"
            )
            logger.critical(
                f"These modifiers were not present in the database: {failed_df['effect'].unique().tolist()}"
            )
            dynamic_df = dynamic_df.loc[~dynamic_df["roll"].isna()]

        return dynamic_df

    def _process_dynamic(
        self, df: pd.DataFrame, static_modifers_mask: pd.Series
    ) -> pd.DataFrame:
        """
        A much more expensive operation

        Uses the regex column to match incoming modifiers to modifiers in the db.
        """
        dynamic_modifier_df = self.dynamic_modifier_df
        dynamic_df = df.loc[~static_modifers_mask]  # Everything not static is dynamic
        if dynamic_df.empty:
            raise Exception("ASDHSDHASDHHSADDSHAD")

        dynamic_df.loc[:, "effect"] = dynamic_df.loc[:, "modifier"]

        dynamic_df = self._get_rolls(dynamic_df.copy())

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
        failed_df = merged_dynamic_df.loc[merged_dynamic_df["roll"].isna()]
        if not failed_df.empty:
            logger.exception(
                "Some modifiers did not find their counterpart in the database."
                " This likely means the modifier is new or has been reworded.\n"
                f"{failed_df[['effect', 'roll']].to_string()}"
            )
            merged_dynamic_df = merged_dynamic_df.loc[~merged_dynamic_df["roll"].isna()]

        def convert_text_roll_to_index(row: pd.DataFrame) -> int:
            text_rolls: str = row["textRolls"]
            if text_rolls != "None":
                text_rolls = text_rolls.split("|")
                roll = text_rolls.index(row["roll"])
            else:
                roll = row["roll"]

            return roll

        merged_dynamic_df.loc[:, "roll"] = merged_dynamic_df.apply(
            convert_text_roll_to_index, axis=1
        )  # The `roll` column now contains a number

        return merged_dynamic_df

    def add_rolls(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self._pre_processing(df.copy())

        static_modifers_mask = df["modifier"].isin(self.static_modifier_df["effect"])

        ready_static_df = self._process_static(df.copy(), static_modifers_mask)
        ready_dynamic_df = self._process_dynamic(df.copy(), static_modifers_mask)

        processed_df = pd.concat(
            (ready_static_df, ready_dynamic_df), axis=0, ignore_index=True
        )  # static and dynamic item modifiers are combined into one dataframe again

        return processed_df
