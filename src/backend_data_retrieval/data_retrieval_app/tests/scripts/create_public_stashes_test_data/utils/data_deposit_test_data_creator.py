import itertools
import json
import os
import random
import uuid
from collections.abc import Iterator
from typing import Any

import pandas as pd

from data_retrieval_app.external_data_retrieval.config import settings


class DataDepositTestDataCreator:
    def __init__(self, n_of_items: int) -> None:
        """Creates a number of items from the data deposit files."""
        self.n_of_items = n_of_items
        self.new_modifier_data_location = (
            "data_retrieval_app/data_deposit/modifier/modifier_data/"
        )
        self.new_item_base_type_data_location = (
            "data_retrieval_app/data_deposit/item_base_type/item_base_type_data/"
        )
        self.output_test_data_location_path = "data_retrieval_app/tests/test_data/"

    def _map_filename_to_actual_name(self, filename: str) -> str:
        # TODO: Needs a global list of supported item names instead of this manual approach
        match filename:
            case "AulsUprising.csv":
                return "Aul's Uprising"
            case "BalanceOfTerror.csv":
                return "The Balance of Terror"
            case "BrutalRestraint.csv":
                return "Brutal Restraint"
            case "ElegantHubris.csv":
                return "Elegant Hubris"
            case "ForbiddenFlame.csv":
                return "Forbidden Flame"
            case "ForbiddenFlesh.csv":
                return "Forbidden Flesh"
            case "ForbiddenShako.csv":
                return "Forbidden Shako"
            case "GloriousVanity.csv":
                return "Glorious Vanity"
            case "GrandSpectrum.csv":
                return "Grand Spectrum"
            case "ImpossibleEscape.csv":
                return "Impossible Escape"
            case "LethalPride.csv":
                return "Lethal Pride"
            case "MilitantFaith.csv":
                return "Militant Faith"
            case "Paradoxica.csv":
                return "Paradoxica"
            case "PrecursorsEmblem.csv":
                return "Precursor's Emblem"
            case "ReplicaDragonfangsFlight.csv":
                return "Replica Dragonfang's Flight"
            case "ShroudOfTheLightless.csv":
                return "Shroud of the Lightless"
            case "SkinOfTheLords.csv":
                return "Skin of the Lords"
            case "SplitPersonality.csv":
                return "Split Personality"
            case "SublimeVision.csv":
                return "Sublime Vision"
            case "ThatWhichWasTaken.csv":
                return "That Which Was Taken"
            case "TheCircleOfAmbition.csv":
                return "Circle of Ambition"
            case "TheCircleOfAnguish.csv":
                return "Circle of Anguish"
            case "TheCircleOfFear.csv":
                return "Circle of Fear"
            case "TheCircleOfGuilt.csv":
                return "Circle of Guilt"
            case "TheCircleOfNostalgia.csv":
                return "Circle of Nostalgia"
            case "TheCircleOfRegret.csv":
                return "Circle of Regret"
            case "TheLightOfMeaning.csv":
                return "The Light Of Meaning"
            case "TheUtmost.csv":
                return "The Utmost"
            case "ThreadOfHope.csv":
                return "Thread of Hope"
            case "Voices.csv":
                return "Voices"
            case "WatchersEye.csv":
                return "Watcher's Eye"
            case _:
                return "Unknown CSV file"

    def _load_data(self, data_location: str) -> Iterator[pd.DataFrame]:
        for file_name in os.listdir(data_location):
            filepath = os.path.join(data_location, file_name)
            df = pd.read_csv(filepath, comment="#", index_col=False)
            with open(filepath) as infile:
                for line in infile:
                    if "#" == line[0]:
                        line.rstrip()
                    else:
                        break

            yield file_name, df

    def _get_roll_index_positions(self, modifier_effect: str) -> list[int]:
        """We need the index of the hashtag(s) and amount of hashtags"""
        roll_symbol = "#"
        index_positions = []
        for i, _ in enumerate(modifier_effect):
            if modifier_effect[i : i + len(roll_symbol)] == roll_symbol:
                index_positions.append(i)
        return index_positions

    def _sort_df_based_on_position(self, modifier_df: pd.DataFrame) -> pd.DataFrame:
        """Sorts the DataFrame based on position."""
        return modifier_df.sort_values(by="position")

    def _group_modifier_df(self, modifier_df: pd.DataFrame) -> pd.DataFrame:
        """
        Groups the modifier based on effect.
        `position` and `textRolls` are combined into lists of
        equal length.

        Omits "static" property and aligns minRoll, maxRoll, and textRolls based on positions.
        """
        modifier_df_sorted = self._sort_df_based_on_position(modifier_df.copy())

        agg_dict = {
            "position": lambda positions: list(set(positions)),
            "unique": lambda unique: (
                list(unique)[0] if not pd.isna(list(unique)[0]) else None
            ),
            "static": lambda static: (
                list(static)[0] if not pd.isna(list(static)[0]) else None
            ),
        }

        if "static" not in modifier_df_sorted.columns:
            del agg_dict["static"]
        # Dynamically add aggregation logic based on the presence of the columns
        if "textRolls" in modifier_df_sorted.columns:
            agg_dict["textRolls"] = lambda rolls: [
                roll if not pd.isna(roll) else None for roll in rolls
            ]

        if "minRoll" in modifier_df_sorted.columns:
            agg_dict["minRoll"] = lambda minRoll: [
                roll if not pd.isna(roll) else None for roll in minRoll
            ]

        if "maxRoll" in modifier_df_sorted.columns:
            agg_dict["maxRoll"] = lambda maxRoll: [
                roll if not pd.isna(roll) else None for roll in maxRoll
            ]

        # Aggregate the DataFrame
        grouped_modifier_df_sorted = modifier_df_sorted.groupby(
            "effect", as_index=False, sort=False
        ).agg(agg_dict)

        return grouped_modifier_df_sorted

    def _compute_random_modifier(self, group_mod_r: pd.Series) -> pd.DataFrame:
        effect = group_mod_r["effect"]
        roll_index_positions = self._get_roll_index_positions(effect)
        # Check if 'position' exists in the row before processing
        if "position" in group_mod_r and isinstance(group_mod_r["position"], list):
            for position in reversed(group_mod_r["position"]):
                # Check if 'minRoll', 'maxRoll', and 'textRolls' exist before accessing them
                min_roll = None
                max_roll = None
                text_rolls = None

                if "minRoll" in group_mod_r and isinstance(
                    group_mod_r["minRoll"], list
                ):
                    min_roll = group_mod_r["minRoll"][position]

                if "maxRoll" in group_mod_r and isinstance(
                    group_mod_r["maxRoll"], list
                ):
                    max_roll = group_mod_r["maxRoll"][position]

                if "textRolls" in group_mod_r and isinstance(
                    group_mod_r["textRolls"], list
                ):
                    text_rolls = group_mod_r["textRolls"][position]

                if pd.notna(min_roll) and pd.notna(max_roll):
                    value = round(random.uniform(float(min_roll), float(max_roll)))
                    effect = (
                        effect[: roll_index_positions[position]]
                        + str(value)
                        + effect[roll_index_positions[position] + 1 :]
                    )
                elif pd.notna(text_rolls):
                    options = text_rolls.split("|")
                    selected = random.choice(options)
                    effect = (
                        effect[: roll_index_positions[position]]
                        + selected
                        + effect[roll_index_positions[position] + 1 :]
                    )

        return effect

    def _replace_question_marks(self, effect: str) -> str:
        """50/50 1. Replace question marks with an empty string or 2. Remove character just before question mark."""
        result = []

        for _, char in enumerate(effect):
            if char == "?":
                if random.choice([True, False]):
                    continue
                else:
                    if result:
                        result.pop()  # Remove the last character added to result
            else:
                result.append(char)

        return "".join(result)

    def _remove_one_plus_minus_sign(self, effect: str) -> str:
        return effect.replace("+-", random.choice(["+", "-"]), 1)

    def _extract_and_transform_modifiers(
        self, modifier_df: pd.DataFrame
    ) -> list[dict[str, Any]]:
        """Extract and transform modifiers from the DataFrame."""
        modifiers = []
        grouped_modifiers = self._group_modifier_df(modifier_df.copy())

        for _, row in grouped_modifiers.iterrows():
            if "static" in grouped_modifiers.columns and row.get("static"):
                modifiers.append(row["effect"])
            else:
                # Compute 3 different dynamic modifiers effect with random values
                for _ in range(3):
                    effect = self._compute_random_modifier(row)
                    effect = self._replace_question_marks(effect)
                    effect = self._remove_one_plus_minus_sign(effect)
                    if effect not in modifiers:
                        modifiers.append(effect)

        return modifiers

    def _check_exists_column(self, df: pd.DataFrame, column_name: str) -> bool:
        """Check if a column exists in the DataFrame."""
        return column_name in df.columns

    def _extract_item_base_types(
        self, item_base_types_df: pd.DataFrame
    ) -> tuple[list, list, list]:
        """Extract basetypes from the DataFrame."""
        base_types = set()
        categories = set()
        sub_categories = set()

        # Check if each column exists before accessing it
        category_exists = self._check_exists_column(item_base_types_df, "category")
        sub_category_exists = self._check_exists_column(
            item_base_types_df, "subCategory"
        )

        for _, row in item_base_types_df.iterrows():
            base_types.add(row["baseType"])
            if category_exists:
                categories.add(row["category"])
            if sub_category_exists:
                sub_categories.add(row["subCategory"])

        return list(base_types), list(categories), list(sub_categories)

    def _create_item_dict(
        self,
        file_name: str,
        modifiers: list[str],
        item_base_types: tuple[list, list, list],
    ) -> dict[str, Any]:
        """Create an item dictionary with attributes and modifiers."""

        base_types, categories, sub_categories = item_base_types

        if len(sub_categories) == 0:
            num_sub_categories = 0
        elif len(sub_categories) == 1:
            num_sub_categories = 1
        else:
            num_sub_categories = random.randint(1, len(sub_categories))

        # Create the item dictionary
        item_data = {
            "verified": True,
            "name": self._map_filename_to_actual_name(file_name),
            "identified": True,
            "league": settings.CURRENT_SOFTCORE_LEAGUE,
            "rarity": "Unique",
            "baseType": random.choice(base_types),
            "extended": [
                {
                    "category": (
                        random.choice(categories) if categories else "amulet"
                    ),  # just add dummy value
                    "subCategory": (
                        random.sample(sub_categories, num_sub_categories)
                        if sub_categories
                        else ["helmet"]  # just add dummy value
                    ),
                    "prefixes": random.randint(0, 99),
                    "suffixes": random.randint(0, 99),
                }
            ],
            "explicitMods": modifiers,
        }

        item_data["id"] = str(uuid.uuid4())  # Generate a unique ID
        return item_data

    def save_to_json(self, items: list[dict[str, Any]], output_file: str):
        """Save the items to a JSON file."""
        with open(output_file, "w") as json_file:
            json.dump(items, json_file, indent=4)

    def create_test_data_with_data_deposit_files(
        self,
    ) -> Iterator[tuple[str, str, list[dict[str, Any]]]]:
        # Load data from both locations and make them cycle indefinitely
        modifier_iterator = self._load_data(self.new_modifier_data_location)
        item_base_type_iterator = itertools.cycle(
            self._load_data(self.new_item_base_type_data_location)
        )

        # Iterate over both at the same time
        for (modifier_file_name, df), (_, item_base_type_df) in zip(
            modifier_iterator, item_base_type_iterator, strict=False
        ):
            items = []
            for _ in range(self.n_of_items):
                modifiers = self._extract_and_transform_modifiers(df)
                item_base_types = self._extract_item_base_types(item_base_type_df)
                item_data = self._create_item_dict(
                    modifier_file_name, modifiers, item_base_types
                )
                items.append(item_data)
            yield (
                modifier_file_name,
                items,
            )
