from backend_api.app.core.schemas.modifier import (
    GroupedModifier,
    ModifierCreate,
    ModifierRoll,
    ModifierUniqueItem,
    ModifierUpdate,
)
from pydantic import TypeAdapter

from data_retrieval_app.data_deposit.data_depositor_base import DataDepositorBase
from data_retrieval_app.data_deposit.modifier.modifier_processing_modules import (
    ModifierRegexCreator,
)
from data_retrieval_app.utils import (
    get_grouped_modifiers,
    get_item_base_type_id_by_name,
    get_uniques_by_name_and_basetype_id,
)


class ModifierDataDepositor(
    DataDepositorBase[GroupedModifier, ModifierCreate, ModifierUpdate]
):
    def __init__(self) -> None:
        super().__init__(data_type="modifier", update_model=ModifierUpdate)
        self.regex_creator = ModifierRegexCreator()

    def _get_current_modifiers(self) -> dict[str, GroupedModifier]:
        modifiers = get_grouped_modifiers(self.pom_auth_headers)

        return {(modifier.effect,): modifier for modifier in modifiers}

    def _check_for_complex_updates(self, new_data, current, updated):
        need_update = False
        update_regex = False
        for new_roll, old_roll in zip(new_data.rolls, current.rolls, strict=True):
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
                if updated.rolls is None:
                    updated.rolls = list[ModifierRoll]()

                updated.rolls.append(updated_roll)
                need_update = True

        if update_regex:
            updated.regex = self.regex_creator.make_regex(
                new_data.effect, updated.rolls
            )
            need_update = True

        return need_update, updated

    def _set_db_state(self):
        self.uniques_by_name_and_basetype_id = get_uniques_by_name_and_basetype_id(
            self.pom_auth_headers
        )
        self.basetype_id_by_name = get_item_base_type_id_by_name(self.pom_auth_headers)

    def _preprocess_data(self, data):
        deposit_modifiers = dict[str, ModifierCreate]()
        uniques = [
            self.uniques_by_name_and_basetype_id[
                (
                    self.logged_file_comments["Unique Name"],
                    self.basetype_id_by_name[basetype],
                )
            ]
            for basetype in self.logged_file_comments["Base Types"].split("|")
        ]
        modifier_uniques = [
            ModifierUniqueItem(uniqueItemId=unique.uniqueItemId) for unique in uniques
        ]
        for modifier in data:
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
                deposit_modifier = ModifierCreate(**modifier, uniques=modifier_uniques)
                deposit_modifiers[modifier["effect"]] = deposit_modifier

            deposit_modifier.rolls.append(roll)

        return TypeAdapter(list[ModifierCreate]).validate_python(
            deposit_modifiers.values()
        )

    def _process_data(self, data):
        self.current_data_by_unique_key = self._get_current_modifiers()
        # data = self._track_comments(data)
        non_duplicate_data = self._remove_duplicates(
            data,
            primary_key="modifierId",
            unique_key="effect",
            skip_fields=["regex", "rolls", "uniques"],
        )
        non_duplicate_data = self.regex_creator.add_regex(non_duplicate_data)
        return non_duplicate_data
