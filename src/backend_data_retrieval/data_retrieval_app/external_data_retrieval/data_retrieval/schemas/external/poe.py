from __future__ import annotations

import re
from typing import TYPE_CHECKING

from pydantic import Field

from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.base import (
    PoeModel,
)
from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.internal.cache import (
    CacheItem,
    CacheStash,
)

if TYPE_CHECKING:
    # To avoid circular imports, while maintaining type hinting
    from data_retrieval_app.external_data_retrieval.detectors.detector_controller import (
        DetectorController,
    )


class ItemModFlags(PoeModel):
    fractured: bool | None = None
    mutated: bool | None = None
    crafted: bool | None = None
    desecrated: bool | None = None
    vestigial: bool | None = None


class ItemMod(PoeModel):
    description: str
    flags: ItemModFlags | None = None


class Extended(PoeModel):
    prefixes: int | None = None
    suffixes: int | None = None


class PoeItem(PoeModel):
    # Basic identity / display
    id: str | None = None
    name: str
    type_line: str = Field(alias="typeLine")
    base_type: str = Field(alias="baseType")
    rarity: str | None = None

    # PoeItem state
    verified: bool
    identified: bool
    corrupted: bool | None = None
    duplicated: bool | None = None
    split: bool | None = None
    fractured: bool | None = None
    synthesised: bool | None = None
    elder: bool | None = None
    shaper: bool | None = None
    searing: bool | None = None
    tangled: bool | None = None
    abyss_jewel: bool | None = Field(
        default=None,
        alias="abyssJewel",
    )
    delve: bool | None = None
    is_relic: bool | None = Field(default=None, alias="isRelic")
    replica: bool | None = None
    ruthless: bool | None = None

    # Level / league
    league: str | None = None
    ilvl: int
    item_level: int | None = Field(default=None, alias="itemLevel")
    monster_level: int | None = Field(default=None, alias="monsterLevel")

    # Inventory dimensions / location
    w: int
    h: int
    x: int | None = None
    y: int | None = None
    inventory_id: str | None = Field(
        default=None,
        alias="inventoryId",
    )

    # Stack information
    stack_size: int | None = Field(default=None, alias="stackSize")
    max_stack_size: int | None = Field(
        default=None,
        alias="maxStackSize",
    )
    stack_size_text: str | None = Field(
        default=None,
        alias="stackSizeText",
    )

    # Visuals
    icon: str
    art_filename: str | None = Field(
        default=None,
        alias="artFilename",
    )
    frame_type: int | None = Field(
        default=None,
        alias="frameType",
    )
    frame_type_id: str | None = Field(
        default=None,
        alias="frameTypeId",
    )

    # Mods
    implicit_mods: list[ItemMod] | None = Field(
        default=None,
        alias="implicitMods",
    )
    explicit_mods: list[ItemMod] | None = Field(
        default=None,
        alias="explicitMods",
    )
    crafted_mods: list[str] | None = Field(
        default=None,
        alias="craftedMods",
    )
    fractured_mods: list[str] | None = Field(
        default=None,
        alias="fracturedMods",
    )
    enchant_mods: list[str] | None = Field(
        default=None,
        alias="enchantMods",
    )
    scourge_mods: list[str] | None = Field(
        default=None,
        alias="scourgeMods",
    )
    crucible_mods: list[str] | None = Field(
        default=None,
        alias="crucibleMods",
    )
    veiled_mods: list[str] | None = Field(
        default=None,
        alias="veiledMods",
    )
    cosmetic_mods: list[str] | None = Field(
        default=None,
        alias="cosmeticMods",
    )
    utility_mods: list[str] | None = Field(
        default=None,
        alias="utilityMods",
    )

    # Categories / misc
    category: dict[str, list[str]] | None = None
    flavour_text: list[str] | None = Field(
        default=None,
        alias="flavourText",
    )
    descr_text: str | None = Field(
        default=None,
        alias="descrText",
    )
    sec_descr_text: str | None = Field(
        default=None,
        alias="secDescrText",
    )
    note: str | None = None
    forum_note: str | None = None

    # Special item data
    extended: Extended | None = None

    # Other flags
    locked_to_character: bool | None = Field(
        default=None,
        alias="lockedToCharacter",
    )
    locked_to_account: bool | None = Field(
        default=None,
        alias="lockedToAccount",
    )

    veiled: bool | None = None
    foreseeing: bool | None = None

    def to_cache(self, detector: DetectorController) -> CacheItem:
        return CacheItem(
            id=self.id, note=self.note, category=detector.get_category(self)
        )

    def __eq__(self, other: CacheItem | object) -> bool:
        if isinstance(other, CacheItem):
            print(other)
            return other.id == self.id and other.note == self.note
        return super().__eq__(other)

    def has_price(self) -> bool:
        return self.note is not None and re.match(
            r"^(~b\/o|~price) [0-9]*[.]?[0-9]+ [^ ]*$", self.note
        )


class Stash(PoeModel):
    id: str

    public: bool

    stash: str | None = None
    stash_type: str = Field(alias="stashType")
    league: str | None = None

    items: list[PoeItem] = Field(default_factory=list)

    def to_cache(self, detector: DetectorController) -> CacheStash:
        return CacheStash(
            league=self.league, items=[item.to_cache(detector) for item in self.items]
        )

    def has_price(self) -> bool:
        return self.stash is not None and re.match(
            r"^(~b\/o|~price) \d+ [^ ]*$", self.stash
        )

    def get_item(self, id: str) -> tuple[int, PoeItem | None]:
        for i, item in enumerate(self.items):
            if item.id == id:
                return i, item

        # this will crash the program if the idx is used
        return len(self.items), None
