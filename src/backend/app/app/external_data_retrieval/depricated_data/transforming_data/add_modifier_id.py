import os
import pandas as pd

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
for filename in os.listdir("new_base_data"):
    temp_df = pd.read_csv(f"new_base_data/{filename}", dtype=str)
    temp_df["filename"] = filename
    modifier_df = pd.concat((modifier_df, temp_df), axis=0, ignore_index=True)

modifier_df["modifierId"] = modifier_df.index

for filename in os.listdir("new_base_data"):
    unique_df = modifier_df.loc[modifier_df["filename"] == filename].drop(
        columns=["filename"]
    )
    unique_df.to_csv(f"new_base_data/{filename}", index=False)
