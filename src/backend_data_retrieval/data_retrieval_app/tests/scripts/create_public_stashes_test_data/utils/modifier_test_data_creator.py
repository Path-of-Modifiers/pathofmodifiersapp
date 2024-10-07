import json
import os
import random
import uuid
from collections.abc import Iterator
from typing import Any

import pandas as pd


class ModifierTestDataCreator:
    def __init__(self, n_of_items: int) -> None:
        """Creates a number of items from the modifier data in files from `self.new_modifier_data_location`."""
        self.n_of_items = n_of_items
        self.new_modifier_data_location = (
            "data_retrieval_app/data_deposit/modifier/modifier_data/"
        )
        self.output_test_data_location_path = "data_retrieval_app/tests/test_data/"

    def _load_modifer_data(self) -> Iterator[pd.DataFrame]:
        for file_name in os.listdir(self.new_modifier_data_location):
            filepath = os.path.join(self.new_modifier_data_location, file_name)
            df = pd.read_csv(filepath, comment="#", index_col=False)
            with open(filepath) as infile:
                for line in infile:
                    if "#" == line[0]:
                        line.rstrip()
                    else:
                        break

            yield file_name[:-4], df

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

                # Handle min/max roll substitution if present
                if pd.notna(min_roll) and pd.notna(max_roll):
                    value = round(random.uniform(float(min_roll), float(max_roll)))
                    effect = (
                        effect[: roll_index_positions[position]]
                        + str(value)
                        + effect[roll_index_positions[position] + 1 :]
                    )
                # Handle textRoll substitution if present
                elif pd.notna(text_rolls):
                    options = text_rolls.split("|")
                    selected = random.choice(options)
                    effect = (
                        effect[: roll_index_positions[position]]
                        + selected
                        + effect[roll_index_positions[position] + 1 :]
                    )

        return effect

    def _extract_modifiers(self, modifier_df: pd.DataFrame) -> list[dict[str, Any]]:
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
                    if effect not in modifiers:
                        modifiers.append(effect)

        return modifiers

    def _create_item_dict(self, file_name: str, modifiers: list[str]) -> dict[str, Any]:
        """Create an item dictionary with attributes and modifiers."""
        item_data = {
            "verified": True,
            "name": file_name,
            "identified": True,
            "explicitMods": modifiers,
        }
        item_data["id"] = str(uuid.uuid4())  # Generate a unique ID
        return item_data

    def save_to_json(self, items: list[dict[str, Any]], output_file: str):
        """Save the items to a JSON file."""
        with open(output_file, "w") as json_file:
            json.dump(items, json_file, indent=4)

    def create_test_data_with_modifier_file(
        self,
    ) -> Iterator[tuple[str, list[dict[str, Any]]]]:
        # Process each DataFrame to create item data
        for file_name, df in self._load_modifer_data():
            items = []
            for _ in range(self.n_of_items):
                modifiers = self._extract_modifiers(df)
                item_data = self._create_item_dict(file_name, modifiers)
                items.append(item_data)
            yield (
                file_name,
                items,
            )
