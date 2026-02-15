import re

import pandas as pd
from pydantic import BaseModel, HttpUrl

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.logs.logger import transform_logger as logger
from data_retrieval_app.utils import bulk_update_data, insert_data

pd.set_option("display.max_colwidth", None)


class ModifierSchema(BaseModel):
    modifierId: int
    position: int
    minRoll: int
    maxRoll: int
    implicit: bool
    explicit: bool
    delve: bool
    fractured: bool
    synthesised: bool
    unique: bool
    corrupted: bool
    enchanted: bool
    veiled: bool
    static: bool
    effect: str
    relatedUniques: str
    textRolls: str
    regex: str
    dynamicallyCreated: bool


class CaranteneModifierSchema(BaseModel):
    effect: str
    relatedUnique: str
    implicit: str
    explicit: str
    delve: str
    fractured: str
    synthesised: str
    unique: str
    corrupted: str
    enchanted: str
    veiled: str
    mutated: str


class RollProcessor:
    @property
    def modifier_df(self) -> pd.DataFrame:
        return self._modifier_df

    @modifier_df.setter
    def modifier_df(self, modifier_df: pd.DataFrame):
        self._modifier_df = modifier_df.drop(["createdAt"], axis=1)

        static_modifier_mask = self._modifier_df["static"] == "True"
        self.static_modifier_df = self._modifier_df.loc[static_modifier_mask]

        self.dynamic_modifier_df = self._modifier_df.loc[~static_modifier_mask]

    def add_modifier_df(self, modifier_df: pd.DataFrame):
        try:
            modifier_df = self.modifier_df
        except AttributeError:
            self.modifier_df = modifier_df

    def _pre_processing(self, df: pd.DataFrame) -> pd.DataFrame:
        df.loc[:, "modifier"] = df[
            "modifier"
        ].replace(
            r"\\n|\n", " ", regex=True
        )  # Replaces newline with a space, so that it does not mess up the regex and matches modifiers in the `modifier` table
        # Removes all rows with no modifier (The Adorned)
        no_modifiers_mask = df["modifier"].isna()
        df = df.loc[~no_modifiers_mask]

        return df

    def _update_related_unique_modifier(self, item_modifier_df: pd.DataFrame) -> None:
        if "relatedUniques" not in item_modifier_df.columns:
            item_modifier_df["relatedUniques"] = ""
        item_modifier_df["relatedUniques"] = (
            item_modifier_df["relatedUniques"].fillna("").astype(str)
        )

        item_modifier_df["related_unique_contains"] = item_modifier_df.apply(
            lambda row: row["name"] in row["relatedUniques"].split("|"), axis=1
        )

        item_modifier_df["relatedUniques"] = item_modifier_df.apply(
            lambda row: f"{row['relatedUniques']}|{row['name']}"
            if not row["related_unique_contains"] and pd.notna(row["name"])
            else row["relatedUniques"],
            axis=1,
        )

        modifier_cols = ModifierSchema.model_fields.keys()

        new_modifiers = item_modifier_df[modifier_cols]
        logger.info(
            f"Updating new modifiers related uniques, count: \n {len(new_modifiers)}"
        )

        bulk_update_data(
            new_modifiers,
            table_name="modifier",
            sub_endpoint="update-related-uniques",
        )

    def _process_static(
        self, df: pd.DataFrame, static_modifers_mask: pd.Series
    ) -> pd.DataFrame:
        """
        Static modifiers must be processed first, to reduce the amount of modifiers
        processed by the much more expensive dynamic modifier processing.
        """
        static_modifier_df = self.static_modifier_df

        static_df = df.loc[static_modifers_mask]
        if static_df.empty:
            return pd.DataFrame(
                columns=static_df.columns.append(static_modifier_df.columns)
            )
        static_df.loc[:, "position"] = "0"
        static_df.loc[:, "effect"] = static_df.loc[:, "modifier"]

        merged_static_df = static_df.merge(
            static_modifier_df, on=["effect", "position"], how="left"
        )

        failed_df = merged_static_df.loc[merged_static_df["static"].isna()]

        if not failed_df.empty:
            logger.debug(
                f"Failed to merge static modifier with modifier in DB.\n{failed_df}"
            )
            # remove all modifiers that failed to merge
            # NOTE this should never happen
            merged_static_df = merged_static_df.loc[~merged_static_df["static"].isna()]

        self._update_related_unique_modifier(merged_static_df)

        return merged_static_df

    def _get_rolls(
        self, dynamic_df: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame | None]:
        """
        Uses regex matching groups to extract the rolls and adds
        the correct effect.
        """

        def extract_rolls(matchobj: re.Match) -> str:
            rolls = [
                roll
                for roll in matchobj.groups()
                if roll not in ["reduced", "increased"]  # because of alternate spelling
            ]

            return "matched" + ":-:".join(rolls)

        dynamic_modifier_df = self.dynamic_modifier_df

        # The process must be broken down into a for-loop as the replacement is unique

        dynamic_w_rolls_df = dynamic_df.copy()
        for effect, regex in dynamic_modifier_df[["effect", "regex"]].itertuples(
            index=False
        ):
            try:
                matched_modifiers = dynamic_df["modifier"].str.replace(
                    regex, extract_rolls, regex=True, case=False
                )
            except Exception as e:
                raise Exception(
                    f"Found unprocessable regex pattern: {regex} \n for effect: {effect} \n error: {e}"
                )
            matched_modifiers_mask = matched_modifiers.str.contains("matched", na=False)

            dynamic_w_rolls_df.loc[matched_modifiers_mask, "effect"] = effect
            dynamic_w_rolls_df.loc[
                matched_modifiers_mask, "roll"
            ] = matched_modifiers.loc[matched_modifiers_mask]

            dynamic_df.loc[matched_modifiers_mask, "modifier"] = pd.NA

        dynamic_w_rolls_df.loc[:, "roll"] = (
            dynamic_w_rolls_df["roll"].str.removeprefix("matched").str.split(":-:")
        )
        del dynamic_df
        dynamic_df = dynamic_w_rolls_df

        # If there are rows in the dataframe which contain empty lists, something has failed
        failed_df = dynamic_df.loc[dynamic_df["roll"].isna()]
        if not failed_df.empty:
            logger.warning(
                "Failed to add rolls to listed modifiers, this likely means"
                " the modifier is carantene, legacy or there was a new expansion."
            )
            logger.warning(
                f"These items have missing modifiers: {failed_df['name'].unique().tolist()}"
            )
            modifiers_failed = failed_df["effect"].unique().tolist()
            logger.warning(
                f"These first 15 modifiers of total {len(modifiers_failed)} were not present in the database: {modifiers_failed[:16]}"
            )
            dynamic_df = dynamic_df.loc[~dynamic_df["roll"].isna()]

        return dynamic_df, failed_df if not failed_df.empty else None

    def insert_carantene_modifiers(self, item_df: pd.DataFrame) -> None:
        # Currently only create carantene mods from mutated items
        mutated_item_df = item_df[item_df["mutated"].astype(str) == "True"]
        if mutated_item_df.empty:
            return None

        def create_carantene_modifiers(item_df: pd.DataFrame) -> pd.DataFrame:
            "Build a DataFrame of carantene modifiers from item data."

            base = item_df.loc[:, ["effect", "name", "mutated"]].copy()

            modifiers = base.assign(
                relatedUnique=lambda df: df["name"],
                explicit=True,
                unique=lambda df: df["name"].notna() & (df["name"] != ""),
            ).reset_index(drop=True)

            return modifiers

        carantene_modifier_cols = CaranteneModifierSchema.model_fields.keys()
        carantene_modifiers = create_carantene_modifiers(mutated_item_df)

        assert isinstance(carantene_modifiers, pd.DataFrame)

        existing_cols = [
            col for col in carantene_modifier_cols if col in carantene_modifiers.columns
        ]
        carantene_modifiers = carantene_modifiers[existing_cols]

        logger.info(
            f"Found {len(carantene_modifiers)} to carantene modifiers, inserting to db..."
        )

        insert_data(
            carantene_modifiers,
            url=HttpUrl(settings.BACKEND_BASE_URL),
            table_name="carantene_modifier",
            logger=logger,
        )

    def _process_dynamic(
        self, df: pd.DataFrame, static_modifers_mask: pd.Series
    ) -> pd.DataFrame:
        """
        A much more expensive operation

        Uses the regex column to match incoming modifiers to modifiers in the db.
        """
        dynamic_modifier_df = self.dynamic_modifier_df
        dynamic_df = df.loc[~static_modifers_mask]  # Everything not static is dynamic
        if dynamic_df.empty:
            return pd.DataFrame(
                columns=dynamic_df.columns.append(dynamic_modifier_df.columns)
            )

        dynamic_df.loc[:, "effect"] = dynamic_df.loc[:, "modifier"]

        dynamic_df, failed_dynamic_df = self._get_rolls(dynamic_df.copy())

        # Creates a column for position, which contains a list of numerical strings
        dynamic_df.loc[:, "position"] = dynamic_df.loc[:, "roll"].apply(
            lambda x: [str(i) for i in range(len(x))]
        )

        # Each row describes one roll
        dynamic_df = dynamic_df.explode(["roll", "position"])

        merged_dynamic_df = dynamic_df.merge(
            dynamic_modifier_df, on=["effect", "position"], how="left"
        )

        # If all of these fields are still NA, it means that modifier was not matched with a modifier in our DB
        if failed_dynamic_df is not None:
            # logger.info(
            #    "Some modifiers did not find their counterpart in the database."
            #    " This likely means the modifier is new or has been reworded.\n"
            #    f"{non_matched_modifier_df[['effect', 'roll']].to_string()}"
            # )
            logger.info(
                f"Checking carantene modifiers from non matched modifiers, count={len(failed_dynamic_df)}"
            )

            self.insert_carantene_modifiers(failed_dynamic_df)

            merged_dynamic_df = merged_dynamic_df.loc[~merged_dynamic_df["roll"].isna()]

        self._update_related_unique_modifier(merged_dynamic_df)

        def convert_text_roll_to_index(row: pd.DataFrame) -> int:
            text_rolls: str = row["textRolls"]
            if text_rolls != "None":
                text_rolls = text_rolls.lower().split("|")
                roll = text_rolls.index(row["roll"].lower())
            else:
                roll = row["roll"]

            return roll

        merged_dynamic_df.loc[:, "roll"] = merged_dynamic_df.apply(
            convert_text_roll_to_index, axis=1
        )  # The `roll` column now contains a number

        return merged_dynamic_df

    def add_rolls(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self._pre_processing(df.copy())

        static_modifers_mask = df["modifier"].isin(self.static_modifier_df["effect"])

        ready_static_df = self._process_static(df.copy(), static_modifers_mask)
        ready_dynamic_df = self._process_dynamic(df.copy(), static_modifers_mask)

        processed_df = pd.concat(
            (ready_static_df, ready_dynamic_df), axis=0, ignore_index=True
        )  # static and dynamic item modifiers are combined into one dataframe again

        return processed_df
