import os
import pandas as pd

modifier_df = pd.DataFrame(
    columns=["minRoll", "maxRoll", "textRolls", "position", "effect", "static", "filename"]
)
for filename in os.listdir("base_data"):
    temp_df = pd.read_csv(f"base_data/{filename}", dtype=str)
    temp_df["filename"] = filename
    modifier_df = pd.concat((modifier_df, temp_df), axis=0, ignore_index=True)

static_modifier_mask = modifier_df["static"] == "True"

dynamic_modifier_df = modifier_df.loc[~static_modifier_mask]
static_modifier_df = modifier_df.loc[static_modifier_mask]

dynamic_modifier_df.loc[:, "effect"] = dynamic_modifier_df["effect"].replace(
    r"\\n|\n", " ", regex=True
)


dynamic_modifier_df["effect"] = dynamic_modifier_df["effect"].str.replace("+", r"\+")

grouped_dynamic_modifier_df = dynamic_modifier_df.groupby("effect", as_index=False).agg(
    {
        "position": lambda positions: [position for position in set(positions)],
        "minRoll": lambda x: [element for element in x if not pd.isna(element)],
        "textRolls": lambda x: [element for element in x if not pd.isna(element)],
    }
)
grouped_dynamic_modifier_df["rolls"] = (
    grouped_dynamic_modifier_df["minRoll"] + grouped_dynamic_modifier_df["textRolls"]
)

def add_regex(row):
    effect = row["effect"]
    positions = row["position"]
    rolls = row["rolls"]
    effect_parts = effect.split("#")
    final_effect = ""
    for i, (position, roll, part) in enumerate(zip(positions, rolls, effect_parts)):
        final_effect += part
        if roll.isnumeric():
            final_effect += "([+-]?([0-9]*[.])?[0-9]+)"
        else:
            try:
                final_effect += f"({row["textRolls"][0].replace("-","|")})"
            except IndexError: # In cases of roll is a float
                final_effect += "([+-]?([0-9]*[.])?[0-9]+)"

    final_effect += "".join(effect_parts[i+1:]) # adds the final part of the effect if there is one
    return final_effect

grouped_dynamic_modifier_df["regex"] = grouped_dynamic_modifier_df.apply(add_regex, axis=1)
grouped_dynamic_modifier_df["regex"] = grouped_dynamic_modifier_df["regex"].str.replace("increased|reduced", r"(increased|reduced)", regex=True)
grouped_dynamic_modifier_df["regex"] = grouped_dynamic_modifier_df["regex"].str.replace("\+", r"(\+|\-)")
# print(grouped_dynamic_modifier_df)
dynamic_modifier_df = dynamic_modifier_df.merge(grouped_dynamic_modifier_df, how="left", on="effect", suffixes=["", "_drop"])
dynamic_modifier_df.drop(columns=["position_drop", "minRoll_drop", "textRolls_drop", "rolls"], inplace=True)
# print(dynamic_modifier_df)
dynamic_modifier_df["effect"] = dynamic_modifier_df["effect"].str.replace(r"\+", "+")

final_df = pd.concat((dynamic_modifier_df, static_modifier_df))
# final_df.to_csv("test.csv", index=False)
for filename in os.listdir("base_data"):
    unique_df = final_df.loc[final_df["filename"] == filename].drop(columns=["filename"])
    unique_df.to_csv(f"new_base_data/{filename}", index=False)
