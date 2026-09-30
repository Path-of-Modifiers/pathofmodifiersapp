import re
from collections import defaultdict

from backend_api.app.core.schemas.item_modifier import (
    ItemModifierCreate,
    ItemModifierRoll,
)
from backend_api.app.core.schemas.modifier import GroupedModifier

from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.external.poe import (
    ItemMod,
    PoeItem,
)
from data_retrieval_app.logs.logger import transform_logger as logger


class RollProcessor:
    def __init__(self, modifiers: dict[str, list[GroupedModifier]]):
        self.modifiers = modifiers

        self.missing_modifiers = defaultdict[str, set[str]](set)

    def _process_dynamic_modifier(
        self, db_mod: GroupedModifier, match: re.Match
    ) -> list[ItemModifierRoll]:
        position = 0
        rolls = list[ItemModifierRoll]()
        for roll in match.groups():
            try:
                if roll in ["reduced", "increased"]:
                    continue

                db_roll = db_mod.rolls[position]
                if db_roll.textRolls is not None:
                    extracted_roll = db_roll.textRolls.index(roll)
                else:
                    extracted_roll = float(roll)

                rolls.append(ItemModifierRoll(position=position, roll=extracted_roll))
                position += 1
            except:
                print(roll, position, db_mod)
                raise

        return rolls

    def _extract_rolls(
        self, modifier: ItemMod, db_modifiers: list[GroupedModifier]
    ) -> ItemModifierCreate | None:
        # pre processing
        effect = modifier.description.replace("\n", " ")

        for db_mod in db_modifiers:
            if db_mod.static:
                if db_mod.effect == effect:
                    static_roll = ItemModifierRoll(position=0)
                    return ItemModifierCreate(
                        modifierId=db_mod.modifierId, rolls=[static_roll]
                    )

            elif (match := db_mod.regex.match(effect)) is not None:
                rolls = self._process_dynamic_modifier(db_mod, match)

                return ItemModifierCreate(modifierId=db_mod.modifierId, rolls=rolls)

        return None

    def extract_modifiers(self, item: PoeItem) -> list[ItemModifierCreate] | None:
        db_modifiers = self.modifiers[item.name]

        extracted_modifiers = list[ItemModifierCreate]()
        if item.name == "The Adorned" and item.explicit_mods is None:
            # rare case where the modifier dissapears completely from the item when it rolls 0
            # This can happen with other items, but they will still have some other mods left over
            item.explicit_mods = [
                ItemMod(
                    description=r"0% increased Effect of Jewel Socket Passive Skills containing Corrupted Magic Jewels"
                )
            ]
        elif item.explicit_mods is None:
            logger.critical(f"An item was found with no explicit mods: {item}")
            return None

        for mod in item.explicit_mods:
            extracted_rolls = self._extract_rolls(mod, db_modifiers)
            if extracted_rolls is None:
                self.missing_modifiers[item.name].add(
                    mod.description.replace("\n", " ")
                )
            else:
                extracted_modifiers.append(extracted_rolls)

        return extracted_modifiers

    def log_missing_modifiers(self):
        logger.critical(
            "Failed to add rolls to listed modifiers, this likely means"
            " the modifier are legacy or there was a new expansion."
            f"Missing modifiers: {self.missing_modifiers}"
        )
