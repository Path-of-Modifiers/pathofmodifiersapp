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

        stash_df["item_id"] = stash_df["items"].apply(
            lambda x: [item["id"] for item in x]
        )  # Extracts item_id out of the items json-object, storing it as a list
        stash_df = stash_df.explode(
            "item_id", ignore_index=True
        )  # Explodes the list, making the stash_df's dimensions equal to the number of items

        item_df = pd.json_normalize(
            json_data, record_path="items"
        )  # Extracts items-json

        item_df["stash_id"] = stash_df["id"]

        self.item_df = item_df

    def _create_modifier_table(self, json_data: list) -> None:
        pass

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

    def _transform_modifier_table(self) -> None:
        pass

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

    def _clean_modifier_table(self):
        pass

    def transform_into_tables(self, json_data):
        self._create_stash_table(json_data=json_data)
        self._create_item_table(json_data=json_data)
        self._create_modifier_table(json_data=json_data)

        self._transform_item_table()
        self._transform_modifier_table()

        self._clean_stash_table()
        self._clean_item_table()
        self._clean_modifier_table()


def main():
    json_data = load_test_data()
    data_transformer = DataTransformer()
    data_transformer.transform_into_tables(json_data=json_data)

    return 0


if __name__ == "__main__":
    main()
