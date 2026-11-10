from __future__ import annotations

import random
from enum import Enum
from types import UnionType
from typing import Any, Literal, Union, get_args, get_origin

from backend_api.app.core.schemas.league import League
from backend_api.app.core.schemas.modifier import GroupedModifier

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.external.poe import (
    ItemMod,
    PoeItem,
)
from data_retrieval_app.pom_api_authentication import get_superuser_token_headers
from data_retrieval_app.tests.external_data_retrieval.utils import (
    make_id,
    make_valid_note,
)
from data_retrieval_app.tests.utils import random_value_by_type


class PoEItemFactory:
    base_url = settings.BACKEND_BASE_URL
    pom_auth_headers = get_superuser_token_headers(base_url)

    def __init__(
        self,
        modifiers: dict[str, dict],
        uniques: list[str],
        bases: dict[str, str],
        icons: dict[str, str],
        leagues: list[League],
        *,
        seed: int | None = None,
    ) -> None:
        self.rng = random.Random(seed)

        self.modifiers = modifiers
        self.uniques = uniques
        self.bases = bases
        self.icons = icons
        self.leagues = [league.name for league in leagues]

    def create(self, *, ctx: dict | None = None) -> PoeItem:
        if ctx is None:
            ctx = {}

        ctx.setdefault("rarity", "Unique")
        ctx.setdefault("identified", True)

        if ctx["rarity"] == "Unique":
            ctx.setdefault("name", self.rng.choice(self.uniques))

        if "name" in ctx:
            bases = self.bases.get(ctx["name"])
            if bases is not None:
                ctx.setdefault("base_type", self.rng.choice(bases))

            icon = self.icons.get(ctx["name"])
            if icon is not None:
                ctx.setdefault("icon", icon)

        if ctx["rarity"] == "Unique" and "name" in ctx:
            modifiers = self.modifiers.get(ctx["name"])
            if modifiers is not None:
                ctx.setdefault(
                    "explicit_mods",
                    self._choose_unique_modifiers(modifiers),
                )
            ctx.setdefault("extended", None)

        ctx.setdefault(
            "explicit_mods",
            [],
        )
        ctx.setdefault(
            "implicit_mods",
            [],
        )

        ctx.setdefault("league", self.rng.choice(self.leagues))
        ctx.setdefault("id", make_id())
        ctx.setdefault("note", make_valid_note(rng=self.rng))

        values: dict[str, Any] = {}

        for field_name, field in PoeItem.model_fields.items():
            if field_name not in ctx:
                value = self._generate_type(
                    field.annotation,
                    field_name=field_name,
                )
            else:
                value = ctx[field_name]

            values[field_name] = value

        return PoeItem.model_validate(values)

    def _choose_unique_modifiers(
        self, available_modifiers: list[GroupedModifier]
    ) -> list[ItemMod]:
        n_avail_modifiers = len(available_modifiers)
        n_modifiers = min(n_avail_modifiers, self.rng.choice(range(1, 7)))

        chosen_modifiers = list[ItemMod]()
        for _ in range(n_modifiers):
            modifier = self.rng.choice(available_modifiers)
            chosen_modifiers.append(
                ItemMod(description=self._fill_in_chosen_modifier(modifier))
            )

        return chosen_modifiers

    def _fill_in_chosen_modifier(self, modifier: GroupedModifier) -> str:
        effect = modifier.effect
        for roll_ctx in modifier.rolls:
            if roll_ctx.textRolls is not None:
                effect = effect.replace("#", self.rng.choice(roll_ctx.textRolls), 1)
            elif roll_ctx.minRoll is not None and roll_ctx.maxRoll is not None:
                effect = effect.replace(
                    "#", str(self.rng.uniform(roll_ctx.minRoll, roll_ctx.maxRoll))
                )

        return effect

    def _generate_type(
        self,
        annotation: Any,
        *,
        field_name: str = "",
    ) -> Any:
        """Generate a value recursively from a Python type annotation."""

        origin = get_origin(annotation)
        args = get_args(annotation)

        # Optional[T] and T | None
        if origin in (Union, UnionType):
            non_none = [t for t in args if t is not type(None)]
            if type(None) in args and self.rng.random() < 0.5:
                return None
            return self._generate_type(
                self.rng.choice(non_none),
                field_name=field_name,
            )

        # Literal values
        if origin is Literal:
            return self.rng.choice(args)

        # Lists, sets, tuples and dictionaries
        if origin in (list, set, frozenset):
            item_type = args[0] if args else Any
            count = self.rng.randint(0, 3)
            items = [
                self._generate_type(item_type, field_name=field_name)
                for _ in range(count)
            ]
            return origin(items)

        if origin is tuple:
            if len(args) == 2 and args[1] is Ellipsis:
                return tuple(
                    self._generate_type(args[0], field_name=field_name)
                    for _ in range(self.rng.randint(0, 3))
                )
            return tuple(
                self._generate_type(arg, field_name=field_name) for arg in args
            )

        if origin is dict:
            key_type, value_type = args or (str, Any)
            return {
                self._generate_type(key_type): self._generate_type(
                    value_type, field_name=field_name
                )
                for _ in range(self.rng.randint(0, 3))
            }

        # Nested Pydantic models
        # if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        #     return self.create(annotation)

        # Enums
        if isinstance(annotation, type) and issubclass(annotation, Enum):
            return self.rng.choice(list(annotation))

        return random_value_by_type(annotation, rng=self.rng, field_name=field_name)
