# import schemas as _schemas
from flatten_json import flatten
import json
import pandas as pd


def load_test_data():
    with open(r"testing_data\2024_01_24 22_28.json", encoding="utf8") as infile:
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

    def _create_modifier_table(self, json_data: list) -> None:
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

    def _transform_modifier_table(self) -> None:
        raise NotImplementedError("Only available in child classes")

    def _clean_stash_table(self):
        self.stash_df.drop(["items", "stashType"], axis=1, inplace=True)

    def _clean_item_table(self):
        item_df = self.item_df.drop(
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
        )

        item_df.to_csv("test.csv", index=False)

    def _clean_item_modifier_table(self):
        raise NotImplementedError("Only available in child classes")

    def _clean_modifier_table(self):
        raise NotImplementedError("Only available in child classes")

    def transform_into_tables(self, json_data):
        self._create_stash_table(json_data=json_data)
        self._create_item_table(json_data=json_data)
        self._create_item_modifier_table(json_data=json_data)
        # self._create_modifier_table(json_data=json_data)

        self._transform_item_table()
        self._transform_item_modifier_table()
        # self._transform_modifier_table()

        self._clean_stash_table()
        self._clean_item_table()
        self._clean_modifier_table()

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
        static_modifier_mask = modifier_df["static"] == "True"
        # print(modifier_df.loc[~static_modifier_mask]["static"].unique())
        # print(modifier_df.loc["static"])
        # quit()

        dynamic_modifier_df = modifier_df.loc[~static_modifier_mask]
        static_modifier_df = modifier_df.loc[static_modifier_mask]

        static_df = df.loc[df["modifier"].isin(static_modifier_df["effect"])]
        static_df["position"] = "0"
        static_df["modifier"] = ""

        dynamic_df = df.loc[~df["modifier"].isin(static_modifier_df["effect"])]

        dynamic_df.loc[:, "modifier"] = dynamic_df["modifier"].replace(
            r"\\n|\n", " ", regex=True
        )
        dynamic_modifier_df.loc[:, "effect"] = dynamic_modifier_df["effect"].replace(
            r"\\n|\n", " ", regex=True
        )

        pattern = (
            dynamic_modifier_df["effect"]
            .drop_duplicates()
            .str.replace("+", r"\+")
            .str.split("#")
            .apply(lambda parts: [part for part in parts if part])
            .explode()
            .sort_values(key=lambda x: -x.str.len())
        )
        # print(
        #     dynamic_df.loc[
        #         dynamic_df["modifier"].str.contains("of Energy Shield on Kill"),
        #         "modifier",
        #     ].iloc[0]
        # )
        # quit()
        dynamic_df["range"] = dynamic_df["modifier"]
        for i in pattern.apply(lambda x: len(x)).tolist():
            small_pattern = "|".join(pattern.loc[pattern.str.len() == i].tolist())
            # print()
            # print(small_pattern)
            # print(dynamic_df.loc[~(dynamic_df["range"] == dynamic_df["modifier"])])
            # print()
            dynamic_df.loc[:, "range"] = dynamic_df["range"].str.replace(
                small_pattern,
                "---",
                regex=True,
            )
            # print(dynamic_df.loc[~(dynamic_df["range"] == dynamic_df["modifier"])])
            # print(dynamic_df.loc[dynamic_df["modifier"].str.contains(small_pattern)])
            # print()
            temp_df = dynamic_df.loc[dynamic_df["modifier"].str.contains(small_pattern)]
            # quit()
            # if not temp_df.empty:
            # if (
            #     temp_df["range"]
            #     .str.contains("of the Stages of your placed Banner")
            #     .any()
            # ):
            # if "chance to take 50% less Area Damage from Hits" in small_pattern:
            # print(temp_df)
            # quit()

        dynamic_df.loc[:, "range"] = dynamic_df["range"].str.split("---")

        dynamic_df.loc[:, "range"] = dynamic_df["range"].apply(
            lambda rolls: [roll for roll in rolls if roll]
        )
        dynamic_df.loc[:, "position"] = dynamic_df["range"].apply(
            lambda rolls: [str(i) for i in range(len(rolls))]
        )

        def replace_range(row):
            modifier = row["modifier"]
            for range in row["range"]:
                modifier = modifier.replace(range, "#")

            return modifier

        dynamic_df.loc[:, "effect"] = dynamic_df.apply(replace_range, axis=1)
        dynamic_df = dynamic_df.explode(["range", "position"])

        joined_df = dynamic_df.merge(
            dynamic_modifier_df, on=["effect", "position"], how="left"
        )

        def func(row):
            x = row["range"]
            if x.isnumeric():
                x = float(x)
                min_roll, max_roll = float(row["minRoll"]), float(row["maxRoll"])
                y = (x - min_roll) / max_roll
            else:
                print(row["textRolls"])
                print(row)
                text_rolls = row["textRolls"].split("-")
                y = text_rolls.index(x) / len(text_rolls)

            return str(y)

        failed_match_df = joined_df.loc[
            joined_df[["minRoll", "maxRoll", "textRolls"]].isna().all(axis=1)
        ]
        print(failed_match_df[["modifier", "effect", "range"]])
        # for modifier in failed_match_df["modifier"].unique():
        #     print(modifier)
        quit()
        # joined_df["range"] = joined_df.apply(func, axis=1)
        # print(joined_df["range"])
        # print(joined_df["name"].unique())
        # joined_df.to_csv("test.csv", index=False)
        # print(
        #     dynamic_modifier_df.loc[
        #         dynamic_modifier_df["effect"]
        #         == r"Carved to glorify # new faithful converted by High Templar #\nPassives in radius are Conquered by the Templars"
        #     ]
        # )
        # print(joined_df["effect"])
        # quit()
        # print(dynamic_modifier_df)
        # print(dynamic_df)

        # new_df = pd.concat((dynamic_df, static_df), ignore_index=True)
        # print(pattern.tolist())
        # df["modifier"] = df["modifier"].str.replace(r"\n", "", regex=True)
        # print(df)
        # for small_pattern in pattern.tolist():
        #     df["modifier"] = df["modifier"].str.replace(
        #         small_pattern, " ", regex=True
        #     )

        # print(df.iloc[0]["modifier"])
        # print(df.loc[df["roll_file_name"] == "SublimeVision"])
        # print(new_df)


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

    def _create_modifier_table(self, json_data: list) -> None:
        pass

    def _transform_item_modifier_table(self) -> None:
        item_modifier_df = self.item_modifier_df

        item_modifier_df["roll_file_name"] = (
            item_modifier_df["name"].str.replace("'", "").str.replace(" ", "")
        )

        modifier_df = pd.DataFrame(
            columns=["minRoll", "maxRoll", "textRolls", "position", "effect", "static"]
        )
        for unique in item_modifier_df["roll_file_name"].unique():
            # if unique != "ThatWhichWasTaken":
            #     continue
            temp_df = pd.read_csv(f"base_data/{unique}.csv", dtype=str)
            modifier_df = pd.concat((modifier_df, temp_df), axis=0, ignore_index=True)

        item_modifier_df = self._get_rolls_data(
            df=item_modifier_df.loc[item_modifier_df["name"] == "Grand Spectrum"],
            # df=item_modifier_df,
            modifier_df=modifier_df,
        )

    def _transform_modifier_table(self) -> None:
        pass

    def _clean_item_modifier_table(self):
        pass

    def _clean_modifier_table(self):
        pass


def main():
    json_data = load_test_data()
    data_transformer = UniqueDataTransformer()
    data_transformer.transform_into_tables(json_data=json_data)

    return 0


if __name__ == "__main__":
    main()
