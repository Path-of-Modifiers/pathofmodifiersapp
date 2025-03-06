import os
import random
from collections.abc import Iterator
from io import StringIO
from typing import Any

import pandas as pd
import requests

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.logs.logger import test_logger
from data_retrieval_app.pom_api_authentication import (
    get_superuser_token_headers,
)
from data_retrieval_app.tests.scripts.create_public_stashes_test_data.config import (
    script_settings,
)
from data_retrieval_app.tests.utils import random_float, random_int


class DataDepositTestDataCreator:
    def __init__(self, n_of_items: int) -> None:
        """
        Creates a number of items from the data deposit files.

        Parameters:
            :n_of_items: (int) Specifies number of items to create per modifier file.
        """
        self.n_of_items = n_of_items
        self.new_modifier_data_location = (
            "data_retrieval_app/data_deposit/modifier/modifier_data/"
        )
        self.output_test_data_location_path = "data_retrieval_app/tests/test_data/"

        if "localhost" not in settings.DOMAIN:
            self.base_url = f"https://{settings.DOMAIN}"
        else:
            self.base_url = "http://src-backend-1"
        self.pom_auth_headers = get_superuser_token_headers(
            self.base_url + "/api/api_v1"
        )

        self.base_type_df = self._get_df_from_url("itemBaseType")
        self.grouped_modifier_df = self._get_df_from_url(
            "modifier/grouped_modifiers_by_effect/"
        )
        self.db_modifier_df = self._get_df_from_url("modifier/").sort_values(
            by=["modifierId", "position"]
        )
        self.modifier_ids_to_effect_map: dict[list[int], str] = {}

        if script_settings.MODIFIER_CSV_FILES_TO_ITERATE:
            test_logger.info(
                f"Only iterating specified modifier csv files: {script_settings.MODIFIER_CSV_FILES_TO_ITERATE}"
            )
            self.filepaths += [
                os.path.join(self.new_modifier_data_location, filename)
                for filename in script_settings.MODIFIER_CSV_FILES_TO_ITERATE
            ]
        else:
            self.filepaths = []
            if script_settings.MODIFIER_CATEGORIES_TO_ITERATE:
                for category in script_settings.MODIFIER_CATEGORIES_TO_ITERATE:
                    self.filepaths += [
                        os.path.join(
                            self.new_modifier_data_location, category, filename
                        )
                        for filename in os.listdir()
                    ]
            else:
                for category in os.listdir(self.new_modifier_data_location):
                    self.filepaths += [
                        os.path.join(
                            self.new_modifier_data_location, category, filename
                        )
                        for filename in os.listdir()
                    ]

    def _get_df_from_url(self, route: str) -> pd.DataFrame:
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        headers.update(self.pom_auth_headers)
        response = requests.get(self.base_url + "/api/api_v1/" + route, headers=headers)
        df = pd.read_json(StringIO(response.text), orient="records")
        return df

    def _get_info_from_modifier_file(
        self,
    ) -> Iterator[tuple[str, dict[str, str], pd.DataFrame]]:
        for filepath in self.filepaths:
            comments = {}
            df = pd.read_csv(filepath, dtype=str, comment="#", index_col=False)
            with open(filepath) as infile:
                for line in infile:
                    if "#" == line[0]:
                        split_line = line[1:].split(": ")
                        comments[split_line[0].strip()] = split_line[1].strip()
                    else:
                        break

            yield filepath, comments, df

    def _parse_comment(
        self, comment: str
    ) -> list[str | int | bool] | dict[str | int, int | list[int]]:
        """
        A recursive method that parses comments into intended python object,
        as described in `data_depost/README.md`.
        """
        comment_type = "dict" if ":" in comment else "list"
        if comment_type == "dict":
            key_value_pairs = comment.split(",")
            output = {}
            for pair in key_value_pairs:
                split_pair = pair.split(":")
                output[eval(split_pair[0])] = self._parse_comment(split_pair[1])
        else:
            list_elements = comment.split("|")
            output = []
            for element in list_elements:
                try:
                    output.append(int(element))
                except ValueError:
                    if element == "True":
                        output.append(True)
                    elif element == "False":
                        output.append(False)
                    else:
                        output.append(element)

        return output

    def _find_connected_modifier_ids_and_rolls(
        self,
        modifier_df: pd.DataFrame,
        modifier_distrubution: dict[int | str, list[int]],
    ) -> tuple[
        dict[int | str, list[list[int]]], dict[int | str, list[tuple[int, int] | str]]
    ]:
        """
        Example input modifier_distrubution dict:
        {
            3: [1],
            "rest": [1]
        }
        Example output connected_modifier_ids_dict:
        {
            3: [
                [1],
                [5, 6]
            ],
            "rest": [
                [1]
            ]
        }
        Example output connected_rolls_dict:
        {
            3: [
                [1, 20],
                "Balbala|Xibaqua"
            ],
            "rest": [
                []
            ]
        }
        Where a list indicates numerical roll and
            minRoll, maxRoll = list[0], list[1]
        And a string indicates text roll, where each
        roll is seperated by `|`
        """

        def get_modifier_ids_rolls_effect(
            row: pd.Series,
        ) -> pd.Series:
            choosable_modifier_ids = row["groupedModifierProperties"]["modifierId"]
            effect = row["effect"]

            df: pd.DataFrame = self.db_modifier_df.loc[
                self.db_modifier_df["effect"] == effect
            ]
            not_static = all(df["static"].isna())
            rolls = []
            if not_static:
                rolls = (
                    df["textRolls"]
                    .where(
                        ~df["textRolls"].isna(),
                        df[["minRoll", "maxRoll"]].agg(
                            lambda row: [
                                float(element)
                                for element in row
                                if not pd.isna(element)
                            ],
                            axis=1,
                        ),
                    )
                    .to_list()
                )

            return pd.Series(
                {
                    "modifier_ids": choosable_modifier_ids,
                    "rolls": rolls,
                    "effect": effect,
                }
            )

        grouped_modifier_df = self.grouped_modifier_df
        prev_key = 0
        connected_modifier_ids_dict = {}
        connected_rolls_dict = {}
        for key in modifier_distrubution:
            upper_bound = key
            if key == "rest":
                upper_bound = len(modifier_df)

            choosable_modifiers_slice = slice(prev_key, upper_bound - 1)
            choosable_modifier_df = modifier_df.loc[choosable_modifiers_slice]

            effects = (
                "^"
                + choosable_modifier_df["effect"].str.replace("+", r"\+").unique()
                + "$"
            )

            # Convert to one long regex string
            effects_to_choose_from = "|".join(effects)
            choosable_effects_mask = grouped_modifier_df["effect"].str.contains(
                effects_to_choose_from, regex=True
            )
            choosable_grouped_modifier_df = grouped_modifier_df.loc[
                choosable_effects_mask
            ]

            modifier_ids_rolls_effect_df = choosable_grouped_modifier_df.apply(
                get_modifier_ids_rolls_effect, axis=1
            )

            modifier_ids: list[list[int]] = modifier_ids_rolls_effect_df[
                "modifier_ids"
            ].to_list()
            connected_modifier_ids_dict[key] = modifier_ids

            rolls = modifier_ids_rolls_effect_df["rolls"].to_list()
            connected_rolls_dict[key] = rolls

            effects: list[list[str]] = modifier_ids_rolls_effect_df["effect"].to_list()
            for modifier_id, effect in zip(modifier_ids, effects, strict=True):
                if tuple(modifier_id) not in self.modifier_ids_to_effect_map:
                    self.modifier_ids_to_effect_map[tuple(modifier_id)] = effect

            prev_key = upper_bound

        return connected_modifier_ids_dict, connected_rolls_dict

    def create_templates(self) -> None:
        self.templates = {}
        for (
            filename,
            modifier_comments,
            modifier_df,
        ) in self._get_info_from_modifier_file():
            modifier_template = {}
            if "Unique Name" in modifier_comments:
                modifier_template["item_name"] = self._parse_comment(
                    modifier_comments["Unique Name"]
                )
                modifier_template["is_unique"] = True
            else:
                modifier_template["is_unique"] = False

            if "Base Types" in modifier_comments:
                modifier_template["base_types"] = self._parse_comment(
                    modifier_comments["Base Types"]
                )
            else:
                modifier_template["base_types"] = [
                    random.choice(self.base_type_df["baseType"].to_list())
                ]

            modifier_template["can_duplicate"] = self._parse_comment(
                modifier_comments["Can have duplicate modifiers"]
            )

            if "Modifier distrubution" in modifier_comments:
                modifier_template["distrubution"] = self._parse_comment(
                    modifier_comments["Modifier distrubution"]
                )
            else:
                modifier_template["distrubution"] = {"rest": 6}

            (
                modifier_template["modifier_ids_to_choose"],
                modifier_template["roll_ranges"],
            ) = self._find_connected_modifier_ids_and_rolls(
                modifier_df, modifier_template["distrubution"]
            )
            # Check for equal lengths taken from:
            # https://stackoverflow.com/questions/35791051/better-way-to-check-if-all-lists-in-a-list-are-the-same-length
            it = iter(
                [
                    modifier_template["can_duplicate"],
                    modifier_template["distrubution"].keys(),
                    modifier_template["modifier_ids_to_choose"].keys(),
                    modifier_template["roll_ranges"].keys(),
                ]
            )
            the_len = len(next(it))
            if not all(len(list_to_compare) == the_len for list_to_compare in it):
                raise AttributeError(
                    f"Something went wrong while creating the template, its not correct: \n {modifier_template}\n Lengths:"
                    + str(
                        [
                            len(modifier_template["can_duplicate"]),
                            len(modifier_template["distrubution"].keys()),
                            len(modifier_template["modifier_ids_to_choose"].keys()),
                            len(modifier_template["roll_ranges"].keys()),
                        ]
                    )
                )

            self.templates[filename] = modifier_template

    def _create_random_note_text(self) -> str:
        cur_types = script_settings.ITEM_NOTE_CURRENCY_TYPES
        r_cur_type = cur_types[random_int(0, len(cur_types) - 1)]

        r_int = round(random.gauss(script_settings.MEAN_ITEM_PRICE, 10), 2)

        note = f"~price {r_int} {r_cur_type}"
        return note

    def _create_effect(self, effect: str, rolls: list[str | list[float]]):
        new_effect = ""
        split_effect = effect.split("#")
        for i, roll in enumerate(rolls):
            effect_part = split_effect[i]
            new_effect += effect_part
            if isinstance(roll, str):
                new_effect += random.choice(roll.split("|"))
            else:
                selected_roll = random_float(roll[0], roll[1])
                if selected_roll < 0:
                    new_effect = new_effect.replace("+", "-")

                    # Probably works, `increased` might be present several times,
                    # but should only be replaced once ¯\_(ツ)_/¯
                    opposite_effect = effect.replace("increased", "reduced")
                    split_effect = opposite_effect.split("#")

                    selected_roll *= -1

                new_effect += f"{selected_roll}"

        return new_effect + split_effect[-1]

    def _choose_and_make_modifiers(
        self,
        template: dict[
            str, list[str | bool] | dict[int | str, list[int | str | list[float]]]
        ],
    ):
        """
        Note: Only works when
            len(can_duplicate)
            ==
            len(distrubution.keys())
            ==
            len(modifier_ids_to_choose.keys())
            ==
            len(roll_ranges.keys())
        """
        can_duplicate = template["can_duplicate"]
        distrubution = template["distrubution"]
        modifier_ids_to_choose = template["modifier_ids_to_choose"]
        roll_ranges = template["roll_ranges"]

        modifiers = []
        for i, key in enumerate(distrubution):
            n_modifiers_to_create: int = random.choice(distrubution[key])

            remove_chosen_modifiers_from_pool: bool = not can_duplicate[i]

            modifier_ids_to_choose_from: list[list[int]] = modifier_ids_to_choose[
                key
            ].copy()
            complementing_roll_ranges: list[str | list[float]] = roll_ranges[key].copy()

            for _ in range(n_modifiers_to_create):
                choice_made = random.choice(range(len(modifier_ids_to_choose_from)))

                chosen_modifier_ids = modifier_ids_to_choose_from[choice_made]
                chosen_rolls = complementing_roll_ranges[choice_made]

                effect = self.modifier_ids_to_effect_map[tuple(chosen_modifier_ids)]

                if chosen_rolls:
                    # equivalent to modifier not being static
                    effect = self._create_effect(effect, chosen_rolls)

                modifiers.append(effect)

                if remove_chosen_modifiers_from_pool or not chosen_rolls:
                    # not chosen_rolls -> static, can't have multiple static modifiers
                    modifier_ids_to_choose_from.pop(choice_made)
                    complementing_roll_ranges.pop(choice_made)

        return modifiers

    def _create_item_dict_from_template(
        self,
        template: dict[
            str, list[str | bool] | dict[int | str, list[int | str | list[float]]]
        ],
    ):
        name = random.choice(template["item_name"])
        rarity = (
            "Unique"
            if template["is_unique"]
            else random.choice(["Normal", "Magic", "Rare"])
        )
        base_type = random.choice(template["base_types"])
        modifiers = self._choose_and_make_modifiers(template)

        item_dict = {
            "verified": True,
            "name": name,
            "identified": True,
            "league": settings.CURRENT_SOFTCORE_LEAGUE,
            "rarity": rarity,
            "baseType": base_type,
            "note": self._create_random_note_text(),
            "extended": [
                {
                    "prefixes": random_int(0, 99),
                    "suffixes": random_int(0, 99),
                }
            ],
            "explicitMods": modifiers,
        }

        return item_dict

    def create_test_data(
        self,
    ) -> Iterator[tuple[str, list[dict[str, Any]]]]:
        for filename, template in self.templates.items():
            stash = []
            for _ in range(self.n_of_items):
                item_dict = self._create_item_dict_from_template(template)
                stash.append(item_dict)
            yield filename, stash


def main() -> int:
    test = DataDepositTestDataCreator(50)
    test.create_templates()
    print(list(test.create_test_data()))
    return 0


if __name__ == "__main__":
    main()
