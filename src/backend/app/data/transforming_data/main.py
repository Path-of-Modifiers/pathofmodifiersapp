# import schemas as _schemas
from flatten_json import flatten
import json
import pandas as pd


def load_test_data():
    """
    Temporary test data loader
    """
    with open("testing_data\\2024_01_24 22_28.json", encoding="utf8") as infile:
        data = json.load(infile)

    return data


class DataTransformer:
    def _create_stash_table(self, json_data: list) -> None:
        """
        Creates the basis of the `stash` table.
        It is not immediately processed in order to save compute power later.
        """
        stash_df = pd.json_normalize(json_data)  # Contains columns of JSON-objects

        self.stash_df = stash_df

    def _create_item_table(self, json_data: list) -> None:
        """
        Creates the basis of the `item` table, using parts of `stash` table.

        The `item` table requires the `stashId` as a foreign key. This is
        why the `stash` table was not immediately processed.
        """
        stash_df = self.stash_df.copy(deep=True)  # Deep copy to avoid damage

        stash_df = self._expand_df(
            stash_df, "items", "id"
        )  # Stretches `stash_df` into the same length as `item_df`

        item_df = pd.json_normalize(
            json_data, record_path="items"
        )  # Extracts items-json

        item_df["stashId"] = stash_df["id"]
        item_df.rename(columns={"id": "itemId"}, inplace=True)

        self.item_df = item_df

    def _create_item_modifier_table(self, json_data: list) -> None:
        """
        The `item_modifier` table heavily relies on what type of item the modifiers
        belong to.
        """
        self.item_modifier_df = pd.DataFrame()
        raise NotImplementedError("Only available in child classes")

    def _transform_item_table(self) -> None:
        """
        The `item` table requires a foreign key to the `currency` table.
        Everything related to the price of the item is stored in the `node`
        attribute.

        There are two types of listings in POE, exact price and asking price which are
        represented by `price` and `b/o` respectively.
        """
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
        """
        The `item_modifier` table heavily relies on what type of item the modifiers
        belong to.
        """
        raise NotImplementedError("Only available in child classes")

    def _clean_stash_table(self):
        """
        Gets rid of unnecessay information, so that only fields needed for the DB remains.
        """
        self.stash_df.drop(["items", "stashType"], axis=1, inplace=True)

    def _clean_item_table(self):
        """
        Gets rid of unnecessay information, so that only fields needed for the DB remains.
        """
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
        """
        The `item_modifier` table heavily relies on what type of item the modifiers
        belong to.

        Gets rid of unnecessay information, so that only fields needed for the DB remains.
        """
        raise NotImplementedError("Only available in child classes")

    def _save_tables_to_files(self):
        """
        Saves the tables into their own file
        """
        tables = {
            "stash": self.stash_df,
            "item": self.item_df,
            "item_modifer": self.item_modifier_df,
        }
        for key in tables:
            tables[key].to_csv(f"transformed_data\\{key}.csv", index=False)

    def transform_into_tables(self, json_data: list) -> None:
        """
        The process of extracting data from the JSON-data, transforming it and cleaning it.
        """
        self._create_stash_table(json_data=json_data)
        self._create_item_table(json_data=json_data)
        self._create_item_modifier_table(json_data=json_data)

        self._transform_item_table()
        self._transform_item_modifier_table()

        self._clean_stash_table()
        self._clean_item_table()
        self._clean_item_modifier_table()

        self._save_tables_to_files()

    @staticmethod
    def _expand_df(
        df: pd.DataFrame, json_column: str, target_column: str
    ) -> pd.DataFrame:
        """
        An independent function that is highly related to the class. Was created as a static method
        because it might be necessary to access from several methods. This turned out to be uneccessary
        """
        df["temp_col"] = df[json_column].apply(
            lambda x: [item[target_column] for item in x]
        )  # Extracts column out of the list_column's json-object, storing it as a list
        df = df.explode(
            "temp_col", ignore_index=True
        )  # Explodes the list, making the df's dimensions equal to the number of items

        return df

    @staticmethod
    def _get_ranges(df: pd.DataFrame, modifier_df: pd.DataFrame) -> pd.DataFrame:
        """
        A very complex function for extracting the range out of the `modifier` field.

        Modifiers can be split into two categories: static and dynamic. A static modifier
        has no range, while a dynamic modifier has one or more ranges.

        Using regex, we can link item modifiers to the already-prepared `modifier` table.
        From there we extract the range based on `minRoll` and `maxRoll` or just `textRolls`
        if the roll is not numerical.

        The formula for calculating the range:
            range = (roll - minRoll)/(maxRoll - minRoll)

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
            quit()

        # ---- Dynamic modifier processing ----
        # A much more expensive process
        dynamic_df = df.loc[
            ~df["modifier"].isin(static_modifier_df["effect"])
        ]  # Everything not static is dynamic

        dynamic_df.loc[:, "effect"] = dynamic_df.loc[:, "modifier"]
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
            df["alternateEffect"] = df["alternateEffect"].str.replace("+#", "-#")
            df["alternateEffect"] = df["alternateEffect"].str.replace(
                "increased", "reduced"
            )
            df.loc[
                df["alternateEffect"] == df["effect"],
                "alternateEffect",
            ] = pd.NA  # Gets rid of unneccesary alternate effects

            return df

        dynamic_df = add_alternate_effect(df=dynamic_df)

        def add_range_roll(row):
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

            ranges = modifier.split("---")

            return [range_roll for range_roll in ranges if range_roll]

        dynamic_df.loc[:, "range"] = dynamic_df.apply(
            add_range_roll, axis=1
        )  # the `roll` modifier is stored in the `range` field temporarily

        # If there are rows in the dataframe which contain empty lists, something has failed
        failed_df = dynamic_df.loc[dynamic_df["range"].str.len() == 0]
        try:
            assert failed_df.empty
        except AssertionError:
            print(failed_df)
            quit()

        # Creates a column for position, which contains a list of numerical strings
        dynamic_df.loc[:, "position"] = dynamic_df.loc[:, "range"].apply(
            lambda x: [str(i) for i in range(len(x))]
        )

        # Each row describes one range
        dynamic_df = dynamic_df.explode(["range", "position"])

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
            print(failed_df)
            quit()

        def convert_range_roll_to_range(row):
            """
            The formula mentioned earlier
            """
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
        )  # The `range` column now truly contains the range

        # ---- Finishing touches ----
        processed_df = pd.concat(
            (merged_dynamic_df, merged_static_df), axis=0, ignore_index=True
        )  # static and dynamic item modifiers are combined into one dataframe again

        return processed_df


class UniqueDataTransformer(DataTransformer):
    def _create_item_modifier_table(self, json_data: list) -> None:
        """
        A similiar process to creating the item table, only this time the
        relevant column contains a list and not a JSON-object
        """
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
        """
        Currently relies on locally stored files to retrieve relevant modifiers
        """
        item_modifier_df = self.item_modifier_df

        # --- Only relevant until we connect to the DB ---
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

        # --- Always relevant ---

        item_modifier_df = self._get_ranges(
            df=item_modifier_df,
            modifier_df=modifier_df,
        )

        self.item_modifier_df = item_modifier_df

    def _clean_item_modifier_table(self):
        """
        Gets rid of unnecessay information, so that only fields needed for the DB remains.
        """
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


def main():
    json_data = load_test_data()
    data_transformer = (
        UniqueDataTransformer()
    )  # eventually a system for sending the right JSON-data to the correct data-transformers need to be implemented
    data_transformer.transform_into_tables(json_data=json_data)

    return 0


if __name__ == "__main__":
    main()
