import re

from backend_api.app.core.schemas.modifier import ModifierCreate, ModifierRoll


class ModifierRegexCreator:
    def make_regex(self, effect: str, rolls: list[ModifierRoll]) -> str:
        regex = effect.replace("+", "[+-]")
        for roll in rolls:
            if roll.textRolls is not None:
                regex = regex.replace("#", f"({"|".join(roll.textRolls)})", 1)
            else:
                regex = regex.replace("#", r"([0-9]*[.]?[0-9]+)", 1)

        regex = re.sub(r"increased|reduced", "(increased|reduced)", regex)

        return rf"^{regex}$"

    def add_regex(self, modifiers: list[ModifierCreate]) -> list[ModifierCreate]:
        for modifier in modifiers:
            if not modifier.static:
                modifier.regex = self.make_regex(modifier.effect, modifier.rolls)

        return modifiers
