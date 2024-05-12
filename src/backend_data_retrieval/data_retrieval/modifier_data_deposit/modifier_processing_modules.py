import logging
import pandas as pd
from typing import Tuple, List, Optional, Dict, Any


logging.basicConfig(
    filename="modifier_data_deposit.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)-8s:%(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def add_regex(modifier_df: pd.DataFrame, logger: logging.Logger) -> pd.DataFrame:
    def divide_modifiers_into_dynamic_static(
        modifier_df: pd.DataFrame,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Simply filters the modifier df based on if the modifier is static or not
        """
        static_modifier_mask = modifier_df["static"] == "True"

        dynamic_modifier_df = modifier_df.loc[~static_modifier_mask]
        static_modifier_df = modifier_df.loc[static_modifier_mask]

        return dynamic_modifier_df, static_modifier_df

    def prepare_df_for_regex(dynamic_modifier_df: pd.DataFrame) -> pd.DataFrame:
        """
        The newline symbol continues to be a pain and is easier to just remove. `+` is a regex flag and must therefor
        be replaced by `\+` to distinguish it as a regular charachter
        """
        dynamic_modifier_df.loc[:, "effect"] = dynamic_modifier_df["effect"].replace(
            r"\\n|\n", " ", regex=True
        )
        dynamic_modifier_df.loc[:, "effect"] = dynamic_modifier_df[
            "effect"
        ].str.replace(
            "+", r"\+"
        )  # Do we need to do the same for `-`? Can other regex flags occur?

        return dynamic_modifier_df

    def group_df(dynamic_modifier_df: pd.DataFrame) -> pd.DataFrame:
        """
        Groups the df by `effect`

        The relevant columns are aggregated by combining into a list, which contains only unique positions,
        and no NA rolls.
        """
        agg_dict = {
            "position": lambda positions: [position for position in set(positions)],
            "minRoll": lambda rolls: [roll for roll in rolls if not pd.isna(roll)],
            "textRolls": lambda rolls: [roll for roll in rolls if not pd.isna(roll)],
        }
        grouped_dynamic_modifier_df = dynamic_modifier_df.groupby(
            "effect", as_index=False
        ).agg(agg_dict)
        return grouped_dynamic_modifier_df

    def create_regex_string_from_row(row):
        """
        row["rolls] is a concatenated list of `minRoll` and `textRolls`. Its length describes
        how many positions the `effect` has.
        The zip function iterates through the arguments until one of them has reached the end.
        Originally the `positions` argument was necessary as `rolls` could contain the `minRoll`
        of two different tiers.

        "([+-]?([0-9]*[.])?[0-9]+)" matches any floats in base 10 and below. This may be replaced by
        a regex matching only numbers within the range.
        f"({row["textRolls"][0].replace("-","|")})" matches all possible text rolls.
        """
        # print(row)
        effect = row["effect"]
        positions = row["position"]
        rolls = row["rolls"]
        effect_parts = effect.split("#")
        final_effect = ""
        for i, (roll, part) in enumerate(zip(rolls, effect_parts)):
            final_effect += part
            try:
                float(roll)
                final_effect += "([+-]?([0-9]*[.])?[0-9]+)"  # catches all floats

            except ValueError:
                final_effect += f"({row['textRolls'][0].replace('-','|')})"
            # if roll.isnumeric():
            #     final_effect += "([+-]?([0-9]*[.])?[0-9]+)"  # catches all floats
            # else:
            #     try:
            #         final_effect += f"({row['textRolls'][0].replace('-','|')})"
            #     except IndexError:  # In cases of roll is a float
            #         final_effect += "([+-]?([0-9]*[.])?[0-9]+)"

        final_effect += "".join(
            effect_parts[i + 1 :]
        )  # adds the final part of the effect if there is one
        return final_effect

    def add_regex_column(grouped_dynamic_modifier_df: pd.DataFrame) -> pd.DataFrame:
        """
        Creats the `rolls` column temporarily, which is a concatenated list of `minRoll` and `textRolls`.
        `maxRoll` is not needed, as we only need to check one of the float rolls if it is numerical or not.

        Then a regex string replaces the `#` depending on the roll which can appear there.
        Additionally, according to an assumption we made (any modifier with a +/- or increased/reduced can have an opposite),
        these signs/words are replaced by a regex which can pick up on both alternatives.

        """
        grouped_dynamic_modifier_df["rolls"] = (
            grouped_dynamic_modifier_df["minRoll"]
            + grouped_dynamic_modifier_df["textRolls"]
        )
        grouped_dynamic_modifier_df["regex"] = grouped_dynamic_modifier_df.apply(
            create_regex_string_from_row, axis=1
        )
        grouped_dynamic_modifier_df["regex"] = grouped_dynamic_modifier_df[
            "regex"
        ].str.replace("increased|reduced", r"(increased|reduced)", regex=True)
        grouped_dynamic_modifier_df["regex"] = grouped_dynamic_modifier_df[
            "regex"
        ].str.replace("\+", r"(\+|\-)")

        return grouped_dynamic_modifier_df

    def grouped_df_to_normal(
        dynamic_modifier_df: pd.DataFrame, grouped_dynamic_modifier_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        The grouped df containing the regex is merged with the pre group dynamic modifier df.
        The merge is based on "left" meaning `dynamic_modifier_df` and on the column `effect`.
        The columns only showing up in both dataframes, except `effect`, are given the suffix `_drop`,
        so that they can easily be removed.
        After this `dynamic_modifier_df` only gets a single more column.
        The `effect` column can then return to normal with `+` instead of `-`
        """
        dynamic_modifier_df = dynamic_modifier_df.merge(
            grouped_dynamic_modifier_df, how="left", on="effect", suffixes=["", "_drop"]
        )
        dynamic_modifier_df.drop(
            columns=["position_drop", "minRoll_drop", "textRolls_drop", "rolls"],
            inplace=True,
        )
        dynamic_modifier_df.loc[:, "effect"] = dynamic_modifier_df[
            "effect"
        ].str.replace(r"\+", "+")

        return dynamic_modifier_df

    def combine_dynamic_static(
        dynamic_modifier_df: pd.DataFrame, static_modifier_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Combines the dynamic_modifier_df and the static modifier_df
        """
        final_df = pd.concat((dynamic_modifier_df, static_modifier_df))
        return final_df

    child_logger = logger.getChild("add_regex")
    child_logger.info("Starting process of adding regex")

    modifier_df_required_columns = [
        "minRoll",
        "maxRoll",
        "textRolls",
        "position",
        "effect",
        "static",
    ]
    modifier_df_columns = modifier_df_required_columns + [
        column
        for column in modifier_df.columns
        if column not in modifier_df_required_columns
    ]
    modifier_df = modifier_df.reindex(columns=modifier_df_columns)

    # child_logger.info("Dividing modifier dataframe into dynamic and static modifiers.")
    dynamic_modifier_df, static_modifier_df = divide_modifiers_into_dynamic_static(
        modifier_df=modifier_df
    )
    # child_logger.info("Successfully divided modifier dataframe.")

    # child_logger.info("Preparing dynamic modifier dataframe for regex conversion.")
    dynamic_modifier_df = prepare_df_for_regex(dynamic_modifier_df=dynamic_modifier_df)
    # child_logger.info("Successfully prepared dynamic modifier dataframe.")

    # child_logger.info("Grouping dynamic modifier dataframe per modifier.")
    grouped_dynamic_modifier_df = group_df(dynamic_modifier_df=dynamic_modifier_df)
    # child_logger.info("Successfully grouped dynamic modifier dataframe.")

    # child_logger.info("Adding regex column to grouped dynamic modifer dataframe.")
    grouped_dynamic_modifier_df = add_regex_column(
        grouped_dynamic_modifier_df=grouped_dynamic_modifier_df
    )
    # child_logger.info(
    #     "Successfully added regex column to grouped dynamic modifer dataframe."
    # )

    # child_logger.info("Converting grouped dynamic modifer dataframe to normal.")
    dynamic_modifier_df = grouped_df_to_normal(
        dynamic_modifier_df=dynamic_modifier_df,
        grouped_dynamic_modifier_df=grouped_dynamic_modifier_df,
    )
    # child_logger.info("Successfully converted grouped dynamic modifer dataframe.")

    # child_logger.info(
    #     "Combining dynamic and static modifers into final modifier dataframe."
    # )
    final_df = combine_dynamic_static(
        dynamic_modifier_df=dynamic_modifier_df, static_modifier_df=static_modifier_df
    )
    # child_logger.info("Successfully combined dynamic and static modifers.")

    child_logger.info("Completed process of adding regex")

    return final_df


def check_for_updated_text_rolls(
    data: Dict[str, Any], row_new: pd.Series, logger: logging.Logger
) -> Tuple[Dict[str, Any], bool]:
    if data["textRolls"] != row_new["textRolls"]:
        logger.info("Found a modifier with new 'textRolls'.")
        data["textRolls"] = row_new["textRolls"]
        put_update = True
    else:
        put_update = False

    return data, put_update


def check_for_updated_numerical_rolls(
    data: Dict[str, Any], row_new: pd.Series, logger: logging.Logger
) -> Tuple[Dict[str, Any], bool]:
    min_roll = data["minRoll"]
    max_roll = data["maxRoll"]

    new_min_roll = row_new["minRoll"]
    new_max_roll = row_new["maxRoll"]

    if float(min_roll) > float(new_min_roll):
        logger.info("Found a modifier with a lower 'minRoll'.")
        data["minRoll"] = new_min_roll

    if float(max_roll) < float(new_max_roll):
        logger.info("Found a modifier with a higher 'maxRoll'.")
        data["maxRoll"] = new_max_roll

    if min_roll != new_min_roll or max_roll != new_max_roll:
        logger.info("Updating modifier to bring numerical roll range up-to-date.")
        put_update = True
    else:
        put_update = False

    return data, put_update


def check_for_additional_modifier_types(
    data: Dict[str, Any],
    row_new: pd.Series,
    put_update: bool,
    modifier_types: List[str],
    logger: logging.Logger,
) -> Tuple[Dict[str, Any], bool]:
    for modifier_type in modifier_types:
        if modifier_type in row_new.index and modifier_type not in data:
            logger.info(f"Added a modifier type to a modifier.")
            data[modifier_type] = row_new[modifier_type]
            put_update = True

    return data, put_update
