import datetime as _dt

import pydantic as _pydantic


class Influences(_pydantic.BaseModel):
    elder: bool | None = None
    shaper: bool | None = None
    crusader: bool | None = None
    redeemer: bool | None = None
    hunter: bool | None = None
    warlord: bool | None = None


# Shared item props
class _BaseItem(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    name: str | None = None
    league: str
    itemBaseTypeId: int
    typeLine: str
    ilvl: int
    rarity: str
    identified: bool = True
    currencyAmount: float | None = None
    currencyId: int | None = None
    corrupted: bool | None = None
    delve: bool | None = None
    fractured: bool | None = None
    synthesised: bool | None = None
    replica: bool | None = None
    influences: Influences | None = None
    searing: bool | None = None
    tangled: bool | None = None
    isRelic: bool | None = None
    prefixes: int | None = None
    suffixes: int | None = None
    foilVariation: int | None = None


# Properties to receive on item creation
class ItemCreate(_BaseItem):
    createdHoursSinceLaunch: int


# Properties to receive on update
class ItemUpdate(_BaseItem):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(_BaseItem):
    createdHoursSinceLaunch: int
    itemId: int


# Properties to return to client
class Item(ItemInDBBase):
    pass


# Properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
