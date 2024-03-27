import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'


def get_rolls(df: pd.DataFrame, modifier_df: pd.DataFrame) -> pd.DataFrame:
    """
    A very complex function for extracting the roll out of the `modifier` field.

    Modifiers can be split into two categories: static and dynamic. A static modifier
    has no roll, while a dynamic modifier has one or more rolls.

    Using regex, we can link item modifiers to the already-prepared `modifier` table.
    From there we extract the roll based on `minRoll` and `maxRoll` or just `textRolls`
    if the roll is not numerical.

    The formula for calculating the roll:
        roll = (roll - minRoll)/(maxRoll - minRoll)

    Where:
        `roll` is extracted from the `modifier` field

        For text rolls, `roll` is the index of roll in a stored list. In this case
        `maxRoll` is the length of the list and `minRoll` is zero

    The method contains assertions to ensure successful steps.
    """
    df.loc[:, "modifier"] = df["modifier"].replace(
        r"\\n|\n", " ", regex=True
    )  # Replaces newline with a space, so that it does not mess up the regex and matches modifiers in the `modifier` table

    # We divide the modifier into the two categories
    static_modifier_mask = modifier_df["static"] == "True"

    dynamic_modifier_df = modifier_df.loc[~static_modifier_mask]
    static_modifier_df = modifier_df.loc[static_modifier_mask]

    # ---- Static modifier processing ----
    # Static modifiers must be processed first, to reduce the amount of modifiers
    # processed by the much more expensive dynamic modifier processing
    static_df = df.loc[df["modifier"].isin(static_modifier_df["effect"])]
    static_df.loc[:, "position"] = "0"
    static_df.loc[:, "effect"] = static_df.loc[:, "modifier"]

    merged_static_df = static_df.merge(
        static_modifier_df, on=["effect", "position"], how="left"
    )
    failed_df = merged_static_df.loc[merged_static_df["static"].isna()]

    # Should never fail, by the nature of the process
    try:
        assert failed_df.empty
    except AssertionError:
        print(failed_df)
        print("Failed to merge static modifier with modifier in DB.")
        quit()

    # ---- Dynamic modifier processing ----
    # A much more expensive process
    dynamic_df = df.loc[
        ~df["modifier"].isin(static_modifier_df["effect"])
    ]  # Everything not static is dynamic

    dynamic_df.loc[:, "effect"] = dynamic_df.loc[:, "modifier"]

    dynamic_modifier_df.sort_values(
        "effect", key=lambda x: x.str.len(), ascending=False, inplace=True
    )
    # The process must be broken down into a for-loop as the replacement is unique
    for regex, effect in dynamic_modifier_df[["regex", "effect"]].itertuples(
        index=False
    ):
        dynamic_df.loc[:, "effect"] = dynamic_df.loc[:, "effect"].str.replace(
            regex, effect, regex=True
        )

    def add_alternate_effect(df):
        """
        Alternate effect is the wording of an effect when the roll is negative

        This assumes all modifiers in the `modifier` table are stored with only
        positive elements.
        """
        df.loc[:, "alternateEffect"] = df["effect"]
        df.loc[:, "alternateEffect"] = df["alternateEffect"].str.replace("+#", "-#")
        df.loc[:, "alternateEffect"] = df["alternateEffect"].str.replace(
            "increased", "reduced"
        )
        df.loc[
            df["alternateEffect"] == df["effect"],
            "alternateEffect",
        ] = pd.NA  # Gets rid of unneccesary alternate effects

        return df

    dynamic_df = add_alternate_effect(df=dynamic_df)

    def add_roll(row):
        """
        The main part of this method.

        The `effect` modifier contains `#` as a placeholder for the `roll`.
        By replacing one part of the `effect` at a time, we end up with
        only the roll and `---`. We then split this into a list, which is
        the filtered to only return elements which are not empty strings.
        """
        modifier = row["modifier"]
        effect = row["effect"]
        effect_parts = [part for part in effect.split("#") if part]

        if not pd.isna(row["alternateEffect"]):
            alternate_effect = row["alternateEffect"]
            effect_parts += [part for part in alternate_effect.split("#") if part]

        for part in effect_parts:
            modifier = modifier.replace(part, "---")

        rolls = modifier.split("---")

        return [roll for roll in rolls if roll]

    dynamic_df.loc[:, "roll"] = dynamic_df.apply(
        add_roll, axis=1
    )  # the `roll` modifier is stored in the `range` field temporarily

    # If there are rows in the dataframe which contain empty lists, something has failed
    failed_df = dynamic_df.loc[dynamic_df["roll"].str.len() == 0]
    try:
        assert failed_df.empty
    except AssertionError:
        print(failed_df)
        print("Failed to merge dynamic modifier with modifier in DB.")
        quit()

    # Creates a column for position, which contains a list of numerical strings
    dynamic_df.loc[:, "position"] = dynamic_df.loc[:, "roll"].apply(
        lambda x: [str(i) for i in range(len(x))]
    )

    # Each row describes one range
    dynamic_df = dynamic_df.explode(["roll", "position"])

    merged_dynamic_df = dynamic_df.merge(
        dynamic_modifier_df, on=["effect", "position"], how="left"
    )

    # If all of these fields are still NA, it means that modifier was not matched with a modifier in our DB
    failed_df = merged_dynamic_df.loc[
        merged_dynamic_df[["minRoll", "maxRoll", "textRolls"]].isna().all(axis=1)
    ]

    try:
        assert failed_df.empty
    except AssertionError:
        print(failed_df.columns)
        print(failed_df[["effect", "minRoll", "maxRoll", "textRolls"]])
        print("Failed to merge dynamic modifier with dynamic modifier in DB.")
        quit()

    # merged_dynamic_df["range"] = merged_dynamic_df.apply(
    #     convert_range_roll_to_range, axis=1
    # )  # The `range` column now truly contains the range

    # ---- Finishing touches ----
    processed_df = pd.concat(
        (merged_dynamic_df, merged_static_df), axis=0, ignore_index=True
    )  # static and dynamic item modifiers are combined into one dataframe again

    return processed_df
