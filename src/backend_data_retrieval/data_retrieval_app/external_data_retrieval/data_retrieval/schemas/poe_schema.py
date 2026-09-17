from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class PoeModel(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )


class CacheItem(PoeModel):
    id: str
    note: str


class CacheStash(PoeModel):
    league: str
    items: list[CacheItem]


class ItemProperty(PoeModel):
    name: str
    values: list[list[Any]]
    display_mode: int | None = Field(default=None, alias="displayMode")
    progress: float | None = None
    type: int | None = None
    suffix: str | None = None
    icon: str | None = None


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


class Item(PoeModel):
    # Basic identity / display
    id: str | None = None
    name: str
    type_line: str = Field(alias="typeLine")
    base_type: str = Field(alias="baseType")
    rarity: str | None = None

    # Item state
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

    # Item properties
    properties: list[ItemProperty] | None = None
    notable_properties: list[ItemProperty] | None = Field(
        default=None,
        alias="notableProperties",
    )
    requirements: list[ItemProperty] | None = None
    additional_properties: list[ItemProperty] | None = Field(
        default=None,
        alias="additionalProperties",
    )
    next_level_requirements: list[ItemProperty] | None = Field(
        default=None,
        alias="nextLevelRequirements",
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

    def to_cache(self) -> CacheItem:
        return CacheItem(id=self.id, note=self.note)

    def __eq__(self, other: CacheItem | object) -> bool:
        if isinstance(other, CacheItem):
            print(other)
            return other.id == self.id and other.note == self.note
        return super().__eq__(other)


class Stash(PoeModel):
    id: str

    public: bool

    stash: str | None = None
    stash_type: str = Field(alias="stashType")
    league: str | None = None

    items: list[Item] = Field(default_factory=list)

    def to_cache(self) -> CacheStash:
        return CacheStash(
            league=self.league, items=[item.to_cache() for item in self.items]
        )

    def get_item(self, id: str) -> tuple[int, Item | None]:
        for i, item in enumerate(self.items):
            if item.id == id:
                return i, item

        # this will crash the program if the idx is used
        return len(self.items), None
