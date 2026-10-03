import pydantic as _pydantic
from backend_api.app.core.schemas.item_modifier import ItemModifierCreate


class Influences(_pydantic.BaseModel):
    elder: bool | None = None
    shaper: bool | None = None
    crusader: bool | None = None
    redeemer: bool | None = None
    hunter: bool | None = None
    warlord: bool | None = None


# Shared item props
class ItemBase(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(
        from_attributes=True, extra="ignore", populate_by_name=True
    )

    gameItemId: str = _pydantic.Field(alias="game_item_id")
    leagueId: int = _pydantic.Field(alias="league_id")

    firstObserved: int = _pydantic.Field(alias="first_observed")

    name: str
    itemBaseTypeId: int = _pydantic.Field(alias="item_base_type_id")
    ilvl: int
    rarity: str

    identified: bool = True
    corrupted: bool | None = None

    fractured: bool | None = None
    synthesised: bool | None = None
    replica: bool | None = None
    influences: Influences | None = None
    searing: bool | None = None
    tangled: bool | None = None


class ItemPrice(_pydantic.BaseModel):
    currencyId: int
    currencyAmount: float
    isAsync: bool | None = None


class ItemCreate(_pydantic.BaseModel):
    item: ItemBase
    price: ItemPrice
    modifiers: list[ItemModifierCreate]


# Properties to receive on update
class ItemUpdate(ItemBase):
    pass


# Properties to return to client
class Item(ItemBase):
    itemId: int


class ItemQuery(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    gameItemId: str
    league: str


# Shared item props
class _BaseItemAvailability(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)
    itemId: int

    currencyId: int
    currencyAmount: float

    validFrom: int
    validTo: int | None = None

    isAsync: bool | None = None


class ItemAvailabilityExpired(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)
    gameItemId: str
    leagueId: int

    validTo: int


class ItemAvailabilityUpdated(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)
    gameItemId: str
    leagueId: int

    price: ItemPrice

    validFrom: int


class ItemAvailability(_BaseItemAvailability):
    availabilityId: int
