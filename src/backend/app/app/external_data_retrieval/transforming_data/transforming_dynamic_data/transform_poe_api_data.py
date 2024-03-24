from typing import List
import pandas as pd


class PoeAPIDataTransformer:

    def _create_account_table(self, df: pd.DataFrame) -> None:
        """
        Creates the basis of the `account` table.
        It is not immediately processed in order to save compute power later.
        """
        self.account_columns = ["accountName"]
        account_df = df.loc[:, self.account_columns]

        self.account_df = account_df

    def _create_stash_table(self, df: pd.DataFrame) -> None:
        """
        Creates the basis of the `stash` table.
        It is not immediately processed in order to save compute power later.
        """
        self.stash_columns = ["stashId", "accountName", "public", "league"]
        stash_df = df.loc[:, self.stash_columns]

        self.stash_df = stash_df

    def _create_item_table(self, df: pd.DataFrame) -> None:
        """
        Creates the basis of the `item` table, using parts of `stash` table.

        The `item` table requires the `stashId` as a foreign key. This is
        why the `stash` table was not immediately processed.
        """
        self.item_columns = [
            "gameItemId",
            "stashId",
            "name",
            "icon",
            "league",
            "typeLine",
            "baseType",
            "rarity",
            "identified",
            "ilvl",
            "forum_note",
            "corrupted",
            "delve",
            "fractured",
            "synthesized",
            "replica",
            "elder",
            "shaper",
            "influences.shaper",
            "influences.elder",
            "influences.crusader",
            "influences.hunter",
            "influences.redeemer",
            "influences.warlord",
            "searing",
            "tangled",
            "foilVariation",
        ]
        item_df = df.loc[
            :, [column for column in self.item_columns if column in df.columns]
        ]  # Can't guarantee all columns are present

        self.item_df = item_df

    def _create_item_modifier_table(
        self, df: pd.DataFrame, modifier_df: pd.DataFrame
    ) -> None:
        """
        The `item_modifier` table heavily relies on what type of item the modifiers
        belong to.
        """
        self.item_modifier_df = pd.DataFrame()
        raise NotImplementedError("Only available in child classes")

    def _transform_account_table(self) -> None:
        # TODO get banned from db
        pass

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
        influence_columns = [
            column for column in item_df.columns if "influences" in column
        ]

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

        def transform_influences(row: pd.DataFrame, influence_columns: List[str]):
            if not row[influence_columns].any():
                return pd.NA
            else:
                influence_dict = {}
                for influence_column in influence_columns:
                    if row[influence_column]:
                        influence_dict[influence_column.replace("influences.", "")] = (
                            True
                        )
                return influence_dict

        item_df["influences"] = item_df.apply(
            lambda row: transform_influences(row, influence_columns), axis=1
        )

        item_df["currencyAmount"] = currency_series.apply(get_currency_amount)
        item_df["currencyType"] = currency_series.apply(get_currency_type)

        self.item_df = item_df

    def _transform_item_modifier_table(self) -> None:
        """
        The `item_modifier` table heavily relies on what type of item the modifiers
        belong to.
        """
        raise NotImplementedError("Only available in child classes")

    def _clean_item_table(self):
        """
        Gets rid of unnecessay information, so that only fields needed for the DB remains.
        """
        drop_list = [
            "influences.shaper",
            "influences.elder",
            "influences.crusader",
            "influences.hunter",
            "influences.redeemer",
            "influences.warlord",
        ]
        self.item_df.drop(
            drop_list,
            axis=1,
            inplace=True,
            errors="ignore",
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
            "account": self.account_df,
        }
        for key in tables:
            tables[key].to_csv(f"transformed_data/{key}.csv", index=False)

    def transform_into_tables(
        self, df: pd.DataFrame, modifier_df: pd.DataFrame
    ) -> None:
        """
        The process of extracting data from the JSON-data, transforming it and cleaning it.
        """
        self._create_stash_table(df)
        self._create_account_table(df)
        self._create_item_table(df)
        self._create_item_modifier_table(df, modifier_df)

        self._transform_item_table()
        self._transform_item_modifier_table()

        self._clean_item_table()
        self._clean_item_modifier_table()

        self._save_tables_to_files()

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
            print("Failed to merge static modifier with modifier in DB.")
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
            print("Failed to merge dynamic modifier with modifier in DB.")
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
            print("Failed to merge dynamic modifier with static modifier in DB.")
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


class UniquePoeAPIDataTransformer(PoeAPIDataTransformer):
    def _create_item_modifier_table(
        self, df: pd.DataFrame, modifier_df: pd.DataFrame
    ) -> None:
        """
        A similiar process to creating the item table, only this time the
        relevant column contains a list and not a JSON-object
        """
        self.item_modifier_columns = ["name", "explicitMods"]

        item_modifier_df = df.loc[:, self.item_modifier_columns]

        item_modifier_df = item_modifier_df.explode("explicitMods")

        self.item_modifier_df = item_modifier_df

    def _transform_item_modifier_table(self) -> None:
        # TODO part of another issue
        pass

    def _clean_item_modifier_table(self):
        """
        Gets rid of unnecessay information, so that only fields needed for the DB remains.
        """
        pass
