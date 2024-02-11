# import schemas as _schemas
from flatten_json import flatten
import json
import pandas as pd


def load_test_data():
    with open("testing_data\\2024_01_24 22_28.json", encoding="utf8") as infile:
        data = json.load(infile)

    return data


class DataTransformer:
    def __init__(self) -> None:
        pass

    def _create_stash_table(self, json_data: list) -> None:
        stash_df = pd.json_normalize(json_data)

        self.stash_df = stash_df

    def _create_item_table(self, json_data: list) -> None:
        stash_df = self.stash_df.copy(deep=True)  # Deep copy to avoid damage

        stash_df = self._expand_df(stash_df, "items", "id")

        item_df = pd.json_normalize(
            json_data, record_path="items"
        )  # Extracts items-json

        item_df["stash_id"] = stash_df["id"]
        item_df.rename(columns={"id": "itemId"}, inplace=True)

        self.item_df = item_df

    def _create_item_modifier_table(self, json_data: list) -> None:
        raise NotImplementedError("Only available in child classes")

    def _transform_item_table(self) -> None:
        item_df = self.item_df
        currency_series = item_df["note"].str.split(" ")

        def get_currency_amount(element):
            if isinstance(element, list):
                return element[1] if element[0] in ["~b/o", "~price"] else pd.NA
            else:
                return pd.NA

        def get_currency_type(element):
            if isinstance(element, list):
                return element[2] if element[0] in ["~b/o", "~price"] else ""
            else:
                return ""

        item_df["currency_amount"] = currency_series.apply(get_currency_amount)
        item_df["currency_type"] = currency_series.apply(get_currency_type)

        self.item_df = item_df

    def _transform_item_modifier_table(self) -> None:
        raise NotImplementedError("Only available in child classes")

    def _clean_stash_table(self):
        self.stash_df.drop(["items", "stashType"], axis=1, inplace=True)

    def _clean_item_table(self):
        self.item_df.drop(
            [
                "verified",
                "w",
                "h",
                "league",
                "descrText",
                "flavourText",
                "frameType",
                "x",
                "y",
                "requirements",
            ],
            axis=1,
            inplace=True,
        )

    def _clean_item_modifier_table(self):
        raise NotImplementedError("Only available in child classes")

    def transform_into_tables(self, json_data):
        self._create_stash_table(json_data=json_data)
        self._create_item_table(json_data=json_data)
        self._create_item_modifier_table(json_data=json_data)

        self._transform_item_table()
        self._transform_item_modifier_table()

        self._clean_stash_table()
        self._clean_item_table()
        self._clean_item_modifier_table()

    @staticmethod
    def _expand_df(df: pd.DataFrame, json_column: str, target_column: str):
        df["temp_col"] = df[json_column].apply(
            lambda x: [item[target_column] for item in x]
        )  # Extracts column out of the list_column's json-object, storing it as a list
        df = df.explode(
            "temp_col", ignore_index=True
        )  # Explodes the list, making the df's dimensions equal to the number of items

        return df

    @staticmethod
    def _get_rolls_data(df, modifier_df):
        df.loc[:, "modifier"] = df["modifier"].replace(r"\\n|\n", " ", regex=True)

        static_modifier_mask = modifier_df["static"] == "True"

        dynamic_modifier_df = modifier_df.loc[~static_modifier_mask]
        static_modifier_df = modifier_df.loc[static_modifier_mask]

        # ---- Static modifier processing ----
        static_df = df.loc[df["modifier"].isin(static_modifier_df["effect"])]
        static_df.loc[:, "position"] = "0"
        static_df.loc[:, "effect"] = static_df.loc[:, "modifier"]

        merged_static_df = static_df.merge(
            static_modifier_df, on=["effect", "position"], how="left"
        )
        failed_df = merged_static_df.loc[merged_static_df["static"].isna()]

        try:
            assert failed_df.empty
        except AssertionError:
            print(failed_df)
            quit()

        # ---- Dynamic modifier processing ----

        dynamic_df = df.loc[~df["modifier"].isin(static_modifier_df["effect"])]

        dynamic_df.loc[:, "effect"] = dynamic_df.loc[:, "modifier"]
        for regex, effect in dynamic_modifier_df[["regex", "effect"]].itertuples(
            index=False
        ):
            dynamic_df.loc[:, "effect"] = dynamic_df.loc[:, "effect"].str.replace(
                regex, effect, regex=True
            )

        def add_alternate_effect(df):
            df.loc[:, "alternateEffect"] = df["effect"]
            df["alternateEffect"] = df["alternateEffect"].str.replace("+#", "-#")
            df["alternateEffect"] = df["alternateEffect"].str.replace(
                "increased", "reduced"
            )
            df.loc[
                df["alternateEffect"] == df["effect"],
                "alternateEffect",
            ] = ""  # Gets rid of unneccesary alternate effects

            return df

        dynamic_df = add_alternate_effect(df=dynamic_df)

        def add_range_roll(row):
            modifier = row["modifier"]
            effect = row["effect"]
            effect_parts = [part for part in effect.split("#") if part]

            if not pd.isna(row["alternateEffect"]):
                alternate_effect = row["alternateEffect"]
                effect_parts += [part for part in alternate_effect.split("#") if part]

            for part in effect_parts:
                modifier = modifier.replace(part, "---")

            ranges = modifier.split("---")

            return [range_roll for range_roll in ranges if range_roll]

        dynamic_df.loc[:, "range"] = dynamic_df.apply(add_range_roll, axis=1)
        failed_df = dynamic_df.loc[dynamic_df["range"].str.len() == 0]
        try:
            assert failed_df.empty
        except AssertionError:
            print(failed_df)
            quit()

        dynamic_df.loc[:, "position"] = dynamic_df.loc[:, "range"].apply(
            lambda x: [str(i) for i in range(len(x))]
        )

        dynamic_df = dynamic_df.explode(["range", "position"])

        merged_dynamic_df = dynamic_df.merge(
            dynamic_modifier_df, on=["effect", "position"], how="left"
        )

        failed_df = merged_dynamic_df.loc[
            merged_dynamic_df[["minRoll", "maxRoll", "textRolls"]].isna().all(axis=1)
        ]

        try:
            assert failed_df.empty
        except AssertionError:
            print(failed_df)
            quit()

        def convert_range_roll_to_range(row):
            un_processed_range = row["range"]
            if not pd.isna(row["textRolls"]):
                text_rolls = row["textRolls"].split("-")
                min_roll = 0
                max_roll = len(text_rolls)
                x = text_rolls.index(un_processed_range)
            else:
                min_roll = float(row["minRoll"])
                max_roll = float(row["maxRoll"])
                x = float(un_processed_range)

            converted_range = (x - min_roll) / (max_roll - min_roll)

            return converted_range

        merged_dynamic_df["range"] = merged_dynamic_df.apply(
            convert_range_roll_to_range, axis=1
        )

        # ---- Finishing touches ----
        processed_df = pd.concat(
            (merged_dynamic_df, merged_static_df), axis=0, ignore_index=True
        )

        finished_df = processed_df.loc[:, ["itemId", "position", "range", "modifierId"]]

        return processed_df


class UniqueDataTransformer(DataTransformer):
    def _create_item_modifier_table(self, json_data: list) -> None:
        item_df = self.item_df.copy(deep=True)

        item_df = item_df.explode("explicitMods", ignore_index=True)

        item_modifier_df = pd.json_normalize(
            json_data, record_path=["items", "explicitMods"]
        )  # Extracts items-json

        item_modifier_df["itemId"] = item_df["itemId"]
        item_modifier_df["name"] = item_df["name"]
        item_modifier_df.rename({0: "modifier"}, axis=1, inplace=True)

        self.item_modifier_df = item_modifier_df

    def _transform_item_modifier_table(self) -> None:
        item_modifier_df = self.item_modifier_df

        item_modifier_df["roll_file_name"] = (
            item_modifier_df["name"].str.replace("'", "").str.replace(" ", "")
        )

        modifier_df = pd.DataFrame(
            columns=[
                "minRoll",
                "maxRoll",
                "textRolls",
                "position",
                "effect",
                "static",
                "modifierId",
            ]
        )
        for unique in item_modifier_df["roll_file_name"].unique():
            # if unique != "WatchersEye":
            #     continue
            temp_df = pd.read_csv(f"new_base_data/{unique}.csv", dtype=str)
            modifier_df = pd.concat((modifier_df, temp_df), axis=0, ignore_index=True)

        item_modifier_df = self._get_rolls_data(
            # df=item_modifier_df.loc[item_modifier_df["name"] == "Watcher's Eye"],
            df=item_modifier_df,
            modifier_df=modifier_df,
        )

        self.item_modifier_df = item_modifier_df

    def _clean_item_modifier_table(self):
        self.item_modifier_df.drop(
            [
                "modifier",
                "name",
                "roll_file_name",
                "effect",
                "alternateEffect",
                "minRoll",
                "maxRoll",
                "textRolls",
                "static",
                "regex",
            ],
            axis=1,
            inplace=True,
        )

        # item_modifier_df = item_modifier_df.loc[
        #     :, ["itemId", "position", "range", "modifierId"]
        # ]


def main():
    json_data = load_test_data()
    data_transformer = UniqueDataTransformer()
    data_transformer.transform_into_tables(json_data=json_data)

    return 0


if __name__ == "__main__":
    main()
