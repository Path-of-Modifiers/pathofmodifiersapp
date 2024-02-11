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

        dynamic_modifier_df = modifier_df.loc[~static_modifier_mask]
        static_modifier_df = modifier_df.loc[static_modifier_mask]

        static_df = df.loc[df["modifier"].isin(static_modifier_df["effect"])]
        static_df["position"] = "0"
        # static_df["modifier"] = ""

        dynamic_df = df.loc[~df["modifier"].isin(static_modifier_df["effect"])]

        dynamic_df.loc[:, "modifier"] = dynamic_df["modifier"].replace(
            r"\\n|\n", " ", regex=True
        )
        dynamic_modifier_df.loc[:, "effect"] = dynamic_modifier_df["effect"].replace(
            r"\\n|\n", " ", regex=True
        )

        
        
        dynamic_modifier_df = dynamic_modifier_df.groupby("effect", as_index=False).agg(
            {
                "position": lambda positions: [position for position in set(positions)],
                "minRoll": lambda x: [element for element in x if not pd.isna(element)],
                "textRolls": lambda x: [element for element in x if not pd.isna(element)],
            }
        )
        dynamic_modifier_df["rolls"] = (
            dynamic_modifier_df["minRoll"] + dynamic_modifier_df["textRolls"]
        )

        dynamic_modifier_df["effect"] = dynamic_modifier_df["effect"].str.replace("+", r"\+")
        dynamic_modifier_df["effect"] = dynamic_modifier_df["effect"].str.replace("-", r"\-")

        def func(row):
            effect = row["effect"]
            positions = row["position"]
            rolls = row["rolls"]
            effect_parts = effect.split("#")
            final_effect = ""
            for i, (position, roll, part) in enumerate(zip(positions, rolls, effect_parts)):
                final_effect += part
                if roll.isnumeric():
                    final_effect += f"(\d+)"
                else:
                    try:
                        final_effect += f"({row["textRolls"][0].replace("-","|")})"
                    except IndexError: # In cases of roll is a float
                        final_effect += f"(\d+)"

            final_effect += "".join(effect_parts[i+1:]) # adds the final part of the effect if there is one
            return final_effect
        
        dynamic_modifier_df["regex"] = dynamic_modifier_df.apply(func, axis=1)
        

        dynamic_df["effect"] = dynamic_df.loc[:, "modifier"]
        for regex, effect in dynamic_modifier_df[["regex", "effect"]].itertuples(index=False):
            dynamic_df["effect"] = dynamic_df.loc[:,"effect"].str.replace(regex, effect, regex=True)

        
        dynamic_df["effect"] = dynamic_df["effect"].str.replace(r"\+", "+")
        
        def func(row):
            modifier = row["modifier"]
            effect = row["effect"]
            effect_parts = [part for part in effect.split("#") if part]
            

            for part in effect_parts:
                modifier = modifier.replace(part, "---")

            ranges = modifier.split("---")

            return [range_roll for range_roll in ranges if range_roll]
        
        dynamic_df["range"] = dynamic_df.apply(func, axis=1)
        failed_df = dynamic_df.loc[dynamic_df["range"].str.len() == 0]
        print(failed_df.iloc[0])
        quit()


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
            if unique != "WatchersEye":
                continue
            temp_df = pd.read_csv(f"base_data/{unique}.csv", dtype=str)
            modifier_df = pd.concat((modifier_df, temp_df), axis=0, ignore_index=True)

        item_modifier_df = self._get_rolls_data(
            df=item_modifier_df.loc[item_modifier_df["name"] == "Watcher's Eye"],
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
