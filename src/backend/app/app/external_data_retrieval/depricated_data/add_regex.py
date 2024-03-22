import os
import pandas as pd


def load_modifiers_from_csv():
    """
    Creates an empty dataframe to establish what columns can show up,
    as some are asymmetric and may therefore not be present always.
    """
    modifier_df = pd.DataFrame(
        columns=[
            "minRoll",
            "maxRoll",
            "textRolls",
            "position",
            "effect",
            "static",
            "filename",
        ]
    )
    for filename in os.listdir("base_data"):
        temp_df = pd.read_csv(f"base_data/{filename}", dtype=str)
        temp_df["filename"] = filename
        modifier_df = pd.concat((modifier_df, temp_df), axis=0, ignore_index=True)

    return modifier_df


def divide_modifiers_into_dynamic_static(modifier_df):
    """
    Simply filters the modifier df based on if the modifier is static or not
    """
    static_modifier_mask = modifier_df["static"] == "True"

    dynamic_modifier_df = modifier_df.loc[~static_modifier_mask]
    static_modifier_df = modifier_df.loc[static_modifier_mask]

    return dynamic_modifier_df, static_modifier_df


def prepare_df_for_regex(dynamic_modifier_df):
    """
    The newline symbol continues to be a pain and is easier to just remove. `+` is a regex flag and must therefor
    be replaced by `\+` to distinguish it as a regular charachter
    """
    dynamic_modifier_df.loc[:, "effect"] = dynamic_modifier_df["effect"].replace(
        r"\\n|\n", " ", regex=True
    )
    dynamic_modifier_df.loc[:, "effect"] = dynamic_modifier_df["effect"].str.replace(
        "+", r"\+"
    )  # Do we need to do the same for `-`? Can other regex flags occur?

    return dynamic_modifier_df


def group_df(dynamic_modifier_df):
    """
    Groups the df by `effect`

    The relevant columns are aggregated by combining into a list, which contains only unique positions,
    and no NA rolls.
    """
    grouped_dynamic_modifier_df = dynamic_modifier_df.groupby(
        "effect", as_index=False
    ).agg(
        {
            "position": lambda positions: [position for position in set(positions)],
            "minRoll": lambda rolls: [roll for roll in rolls if not pd.isna(roll)],
            "textRolls": lambda rolls: [roll for roll in rolls if not pd.isna(roll)],
        }
    )
    return grouped_dynamic_modifier_df


def add_regex_column(grouped_dynamic_modifier_df):
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


def return_grouped_df_to_normal(dynamic_modifier_df, grouped_dynamic_modifier_df):
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
    dynamic_modifier_df.loc[:, "effect"] = dynamic_modifier_df["effect"].str.replace(
        r"\+", "+"
    )

    return dynamic_modifier_df


def combine_dynamic_static(dynamic_modifier_df, static_modifier_df):
    """
    Combines the dynamic_modifier_df and the static modifier_df
    """
    final_df = pd.concat((dynamic_modifier_df, static_modifier_df))
    return final_df


def save_df_to_csv(final_df):
    """
    Saves the processed data into a new folder, named `new_base_data`
    """
    for filename in os.listdir("base_data"):
        unique_df = final_df.loc[final_df["filename"] == filename].drop(
            columns=["filename"]
        )
        unique_df.to_csv(f"new_base_data/{filename}", index=False)


def main():
    modifier_df = load_modifiers_from_csv()
    dynamic_modifier_df, static_modifier_df = divide_modifiers_into_dynamic_static(
        modifier_df=modifier_df
    )
    dynamic_modifier_df = prepare_df_for_regex(dynamic_modifier_df=dynamic_modifier_df)
    grouped_dynamic_modifier_df = group_df(dynamic_modifier_df=dynamic_modifier_df)
    grouped_dynamic_modifier_df = add_regex_column(
        grouped_dynamic_modifier_df=grouped_dynamic_modifier_df
    )
    dynamic_modifier_df = return_grouped_df_to_normal(
        dynamic_modifier_df=dynamic_modifier_df,
        grouped_dynamic_modifier_df=grouped_dynamic_modifier_df,
    )
    final_df = combine_dynamic_static(
        dynamic_modifier_df=dynamic_modifier_df, static_modifier_df=static_modifier_df
    )
    save_df_to_csv(final_df=final_df)


main()
