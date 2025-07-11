import re
from typing import Any

import pandas as pd

from data_retrieval_app.logs.logger import data_deposit_logger as logger


class ModifierRegexCreator:
    def __init__(self):
        self.modifier_df_required_columns = [
            "minRoll",
            "maxRoll",
            "textRolls",
            "position",
            "effect",
            "static",
        ]

    def _divide_into_dynamic_static(
        self, modifier_df: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Divides the modifier dataframe based on the `static` attribute.
        """
        logger.debug("Dividing modifier dataframe into dynamic and static modifiers")

        static_modifier_mask = modifier_df["static"] == "True"

        dynamic_modifier_df = (
            modifier_df.loc[~static_modifier_mask].copy().reset_index()
        )
        static_modifier_df = modifier_df.loc[static_modifier_mask].copy().reset_index()

        logger.debug("Successfully divided modifier dataframe")

        return dynamic_modifier_df, static_modifier_df

    def _prepare_df(self, dynamic_modifier_df: pd.DataFrame) -> pd.DataFrame:
        """
        Escapes the `+`, as it is a regex quantifier.
        """
        dynamic_modifier_df["effect"] = dynamic_modifier_df["effect"].str.replace(
            "+", r"\+"
        )  # Do we need to do the same for `-`? Can other regex symbols occur?

        return dynamic_modifier_df

    def _pre_process(
        self, modifier_df: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Performs pre-process steps:
        1. The program assumes certain columns are present to work. These
           columns are filled with `pd.NA` if not present.
        2a. Divides the modifiers based on their `static` attribute.
        2b. Returns only the static modifier df if no dyamic modifiers
            are found.
        3. Prepares the dynamic modifier df for regex steps.
        """
        modifier_df = modifier_df.reindex(
            columns=modifier_df.columns.union(self.modifier_df_required_columns)
        )

        dynamic_modifier_df, static_modifier_df = self._divide_into_dynamic_static(
            modifier_df=modifier_df
        )
        if dynamic_modifier_df.empty:
            logger.debug("Only static modifiers present")
            return None, static_modifier_df

        dynamic_modifier_df = self._prepare_df(dynamic_modifier_df.copy())
        logger.debug("Finished pre-processing steps")

        return dynamic_modifier_df, static_modifier_df

    def _group_df(self, dynamic_modifier_df: pd.DataFrame) -> pd.DataFrame:
        """
        Groups the dynamic modifier based on effect.
        `position` and `textRolls` are combined into lists of
        equal length.
        """
        logger.debug(
            "Preparing dynamic modifier dataframe for regex conversion, by grouping by effect"
        )
        agg_dict = {
            "position": lambda positions: list(set(positions)),
            "textRolls": lambda rolls: [
                roll if not pd.isna(roll) else None for roll in rolls
            ],
        }
        grouped_dynamic_modifier_df = dynamic_modifier_df.groupby(
            "effect", as_index=False, sort=False
        ).agg(agg_dict)
        logger.debug("Successfully grouped modifiers by effect")

        return grouped_dynamic_modifier_df

    def create_regex_from_row(self, row: pd.DataFrame | dict) -> pd.DataFrame:
        """
        A method available for both internal and external use.

        Uses the aggregated `textRolls` field to determine wether
        the corresponding position has a numerical (textRoll is None),
        or a text roll which determines the regex pattern to insert in
         place of the `#`.

        Then it accounts for alternative spelling (eg. `-` instead of `+` or
         `reduced` instead of `increased`)
        """
        effect: str = row["effect"]
        text_rolls: list[str] = row["textRolls"]

        for text_roll in text_rolls:
            if text_roll is not None:
                effect = effect.replace("#", f"({text_roll})", 1)
            else:
                effect = effect.replace("#", r"([0-9]*[.]?[0-9]+)", 1)

        regex = effect.replace(r"\+", r"[+-]")
        regex = re.sub(r"increased|reduced", "(increased|reduced)", regex)

        return rf"^{regex}$"

    def _unnest_df(
        self,
        dynamic_modifier_df: pd.DataFrame,
        grouped_dynamic_modifier_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Unnests the grouped modfifier dataframe to original shape.
        """
        logger.debug("Reverting the grouped dynamic modifier group to original shape")
        exploded_grouped_dynamic_modifier_df = grouped_dynamic_modifier_df.explode(
            "position", ignore_index=True
        )

        dynamic_modifier_df["regex"] = exploded_grouped_dynamic_modifier_df["regex"]
        logger.debug("Reverted to original shape")

        return dynamic_modifier_df

    def _add_regex(self, dynamic_modifier_df: pd.DataFrame) -> pd.DataFrame:
        """
        Performs the actual steps of adding regex:
        1. Groups the modifiers for easier processing.
        2. Creates the regex by iterating over each row.
        3. Accounts for alternative wording.
        4. Unnests the grouped modfifier dataframe to original shape.
        """
        grouped_dynamic_modifier_df = self._group_df(dynamic_modifier_df.copy())

        logger.debug("Adding regex row by row")
        grouped_dynamic_modifier_df["regex"] = grouped_dynamic_modifier_df.apply(
            self.create_regex_from_row, axis=1
        )

        dynamic_modifier_df = self._unnest_df(
            dynamic_modifier_df.copy(), grouped_dynamic_modifier_df.copy()
        )
        failed_df = dynamic_modifier_df.loc[dynamic_modifier_df["regex"].isna()]
        if not failed_df.empty:
            logger.critical("Some modifiers did not get a regex:")
            logger.critical(failed_df["effect"])
            raise AssertionError("Some modifiers did not get a regex.")
        logger.debug("Successfully added regex row by row")

        return dynamic_modifier_df

    def _post_process(
        self, dynamic_modifier_df: pd.DataFrame, static_modifier_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Undos temporary changes.

        Combines dynamic and static modifiers to one modifier dataframe again.
        """
        dynamic_modifier_df.loc[:, "effect"] = dynamic_modifier_df[
            "effect"
        ].str.replace(r"\+", "+")

        def remove_quantifier(ser: pd.Series) -> pd.Series:
            contains_q_mask = ser.str.contains("?", regex=False)
            ser_contains_q = ser.loc[contains_q_mask]

            if ser_contains_q.empty:
                return ser

            ser_split = ser_contains_q.str.split("?")
            for index, str_parts in ser_split.items():
                ser.iloc[index] = "".join(
                    [
                        part[:-1] if i < (len(str_parts) - 1) else part
                        for i, part in enumerate(str_parts)
                    ]
                )
            return ser

        dynamic_modifier_df.loc[:, "effect"] = remove_quantifier(
            dynamic_modifier_df.loc[:, "effect"]
        )

        final_df = pd.concat(
            (dynamic_modifier_df, static_modifier_df), ignore_index=True
        )

        return final_df

    def add_regex(self, modifier_df: pd.DataFrame) -> pd.DataFrame:
        """
        Processes the incoming dataframe, making it ready for adding regex.
        If no dynamic modifiers are present, it returns early.
        Otherwise, regex is added and post processing steps are applied
        to convert the dataframe back to original shape.
        """
        dynamic_modifier_df, static_modifier_df = self._pre_process(modifier_df.copy())
        if dynamic_modifier_df is None:
            return static_modifier_df

        dynamic_modifier_df = self._add_regex(dynamic_modifier_df.copy())

        logger.debug("Finishing up the regex addition step")
        final_df = self._post_process(
            dynamic_modifier_df.copy(), static_modifier_df.copy()
        )
        logger.debug("Finished adding regex.")

        return final_df


def check_for_updated_text_rolls(
    data: dict[str, Any],
    row_new: pd.DataFrame,
    rolls: list[int | str],
    regex_creator: ModifierRegexCreator,
) -> tuple[dict[str, Any], bool]:
    if data["textRolls"] != row_new["textRolls"]:
        logger.info(
            f"Found a modifier with new 'textRolls'. Modifier: {data['effect']}"
        )
        data["textRolls"] = row_new["textRolls"]
        if rolls is not None:
            data["rolls"] = rolls
            data["effect"] = data["effect"].replace("+", r"\+")
            data["regex"] = regex_creator.create_regex_from_row(data)

            data["effect"] = data["effect"].replace(r"\+", "+")
            data.pop("rolls")

        put_update = True
    else:
        put_update = False

    return data, put_update


def check_for_updated_numerical_rolls(
    data: dict[str, Any], row_new: pd.DataFrame
) -> tuple[dict[str, Any], bool]:
    min_roll = data["minRoll"]
    max_roll = data["maxRoll"]

    new_min_roll = row_new["minRoll"]
    new_max_roll = row_new["maxRoll"]

    if float(min_roll) > float(new_min_roll):
        logger.debug(
            f"Found a modifier with a lower 'minRoll'. Modifier: {data['effect']}"
        )
        data["minRoll"] = new_min_roll

    if float(max_roll) < float(new_max_roll):
        logger.info(
            f"Found a modifier with a higher 'maxRoll'. Modifier: {data['effect']}"
        )
        data["maxRoll"] = new_max_roll

    if min_roll != new_min_roll or max_roll != new_max_roll:
        logger.debug("Updating modifier to bring numerical roll range up-to-date.")
        put_update = True
    else:
        put_update = False

    return data, put_update


def check_for_additional_modifier_types(
    data: dict[str, Any],
    row_new: pd.Series,
    put_update: bool,
    modifier_types: list[str],
) -> tuple[dict[str, Any], bool]:
    for modifier_type in modifier_types:
        if modifier_type in row_new.index and modifier_type not in data:
            logger.info(
                f"Added a modifier type to a modifier. Modifier: {data['effect']}"
            )
            data[modifier_type] = row_new[modifier_type]
            put_update = True

    return data, put_update


def check_for_new_related_unique(
    data: dict[str, Any], put_update: bool, new_related_unique: str
) -> tuple[dict[str, Any], bool]:
    if new_related_unique not in data["relatedUniques"]:
        data["relatedUniques"] += "|" + new_related_unique
        put_update = True

    return data, put_update
