import os
from collections.abc import Iterator
from pathlib import Path

from backend_api.app.core.schemas.modifier import (
    GroupedModifier,
    ModifierCreate,
    ModifierRoll,
    ModifierUpdate,
)
from pydantic import TypeAdapter

from data_retrieval_app.data_deposit.data_depositor_base import DataDepositorBase
from data_retrieval_app.data_deposit.modifier.modifier_processing_modules import (
    ModifierRegexCreator,
)
from data_retrieval_app.data_deposit.utils import read_csv
from data_retrieval_app.logs.logger import data_deposit_logger as logger
from data_retrieval_app.utils import get_grouped_modifiers, send_request_safe


class ModifierDataDepositor(DataDepositorBase):
    def __init__(self) -> None:
        super().__init__(data_type="modifier")
        self.regex_creator = ModifierRegexCreator()

    def _get_current_modifiers(self) -> dict[str, GroupedModifier]:
        modifiers = get_grouped_modifiers(self.pom_auth_headers)

        return {modifier.effect: modifier for modifier in modifiers}

    def _check_for_updates(
        self, modifier: ModifierCreate, current_modifier: GroupedModifier
    ):
        need_update = False
        updated_modifier = ModifierUpdate(modifierId=current_modifier.modifierId)
        for field in modifier.model_fields:
            if field == "relatedUniques":
                new = modifier.relatedUniques.split("|")
                old = current_modifier.relatedUniques.split("|")
                related_uniques = set(new).difference(set(old))
                if related_uniques:
                    updated_modifier.relatedUniques = "|".join(set(new) | set(old))
                    need_update = True

                continue

            if field in ("regex", "rolls"):
                continue

            new = getattr(modifier, field)
            old = getattr(current_modifier, field)
            if not (new == old or (isinstance(old, bool) and old)):
                # update rows which have a different value
                # ignore rows which are bools that are already True
                setattr(updated_modifier, field, new)
                need_update = True

        update_regex = False
        for new_roll, old_roll in zip(
            modifier.rolls, current_modifier.rolls, strict=True
        ):
            updated_roll = ModifierRoll(position=new_roll.position)
            roll_need_update = False
            if new_roll.minRoll is not None and new_roll.minRoll < old_roll.minRoll:
                updated_roll.minRoll = new_roll.minRoll
                roll_need_update = True

            if new_roll.maxRoll is not None and new_roll.maxRoll > old_roll.maxRoll:
                updated_roll.maxRoll = new_roll.maxRoll
                roll_need_update = True

            if new_roll.textRolls is not None:
                text_rolls = set(new_roll.textRolls).difference(set(old_roll.textRolls))
                if text_rolls:
                    # preserve order to not disturb existing data
                    updated_roll.textRolls = old_roll.textRolls + list(text_rolls)
                    roll_need_update = True
                    update_regex = True  # regex contains text rolls

            if roll_need_update:
                if updated_modifier.rolls is None:
                    updated_modifier.rolls = list[ModifierRoll]()

                updated_modifier.rolls.append(updated_roll)
                need_update = True

        if update_regex:
            updated_modifier.regex = self.regex_creator.make_regex(
                modifier.effect, updated_modifier.rolls
            )
            need_update = True

        if need_update:
            send_request_safe(
                "put",
                self.data_url,
                json=updated_modifier.model_dump(exclude_none=True, exclude_unset=True),
                headers=self.pom_auth_headers,
                logger=logger,
            )

        return need_update

    def _remove_duplicates(
        self, modifiers: list[ModifierCreate]
    ) -> list[ModifierCreate]:
        current_modifiers = self._get_current_modifiers()

        previous_effects = list[str]()
        did_update = False
        for modifier in modifiers[:]:
            if modifier.effect in current_modifiers:
                did_update = self._check_for_updates(
                    modifier, current_modifiers[modifier.effect]
                )
                modifiers.remove(modifier)
                continue

            if modifier.effect in previous_effects:
                modifiers.remove(modifier)
                continue

            previous_effects.append(modifier.effect)
        if did_update:
            logger.info("Updated modifiers using new data")
        return modifiers

    def _track_comments(self, modifiers: list[ModifierCreate]) -> list[ModifierCreate]:
        unique_name = self.logged_file_comments["Unique Name"]
        for modifier in modifiers:
            modifier.relatedUniques = unique_name

        return modifiers

    def _load_data(self) -> Iterator[ModifierCreate]:
        for filename in os.listdir(self.new_data_location):
            modifiers = list[dict[str, str]]()
            filepath = Path(self.new_data_location, filename)

            logger.info(f"Loading new data from '{filename}'.")
            more_modifiers, self.logged_file_comments = read_csv(
                filepath, logger=logger
            )
            modifiers.extend(more_modifiers)

            deposit_modifiers = dict[str, ModifierCreate]()
            for modifier in modifiers:
                for key in list(modifier.keys()):
                    if modifier[key] == "":
                        modifier.pop(key)

                text_roll: str | None = modifier.get("textRolls")
                if text_roll is not None:
                    text_roll = text_roll.split("|")

                roll = ModifierRoll(
                    position=modifier["position"],
                    minRoll=modifier.get("minRoll"),
                    maxRoll=modifier.get("maxRoll"),
                    textRolls=text_roll,
                )

                deposit_modifier = deposit_modifiers.get(modifier["effect"])
                if deposit_modifier is None:
                    deposit_modifier = ModifierCreate(**modifier)
                    deposit_modifiers[modifier["effect"]] = deposit_modifier

                deposit_modifier.rolls.append(roll)

            yield TypeAdapter(list[ModifierCreate]).validate_python(
                deposit_modifiers.values()
            )

    def _process_data(self, modifiers: list[ModifierCreate]) -> list[ModifierCreate]:
        modifiers = self.regex_creator.add_regex(modifiers)
        modifiers = self._track_comments(modifiers)
        modifiers = self._remove_duplicates(modifiers)
        return modifiers

    def _insert_data(self, modifiers: list[ModifierCreate]):
        if not modifiers:
            return

        logger.info("Inserting data into database.")
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        headers.update(self.pom_auth_headers)

        send_request_safe(
            "post",
            self.data_url,
            json=TypeAdapter(list[ModifierCreate]).dump_python(modifiers),
            headers=headers,
        )

        logger.info("Successfully inserted data into database.")
