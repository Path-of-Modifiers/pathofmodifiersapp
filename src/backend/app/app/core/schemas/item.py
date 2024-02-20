import datetime as _dt
from typing import Optional
import pydantic as _pydantic


class Influences(_pydantic.BaseModel):
    elder: Optional[bool]
    shaper: Optional[bool]
    crusader: Optional[bool]
    redeemer: Optional[bool]
    hunter: Optional[bool]
    warlord: Optional[bool]


# Shared item props
class _BaseItem(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    gameItemId: str
    stashId: str
    name: Optional[str]
    iconUrl: Optional[str]
    league: str
    typeLine: str
    baseType: str
    rarity: str
    identified: bool
    itemLevel: int
    forumNote: Optional[str]
    currencyAmount: Optional[float]
    currencyId: Optional[int]
    corrupted: Optional[bool]
    delve: Optional[bool]
    fractured: Optional[bool]
    synthesized: Optional[bool]
    replica: Optional[bool]
    elder: Optional[bool]
    shaper: Optional[bool]
    influences: Optional[list[Influences]]
    searing: Optional[bool]
    tangled: Optional[bool]
    isRelic: Optional[bool]
    prefixes: Optional[int]
    suffixes: Optional[int]
    foilVariation: Optional[int]
    inventoryId: Optional[str]


# Properties to receive on item creation
class ItemCreate(_BaseItem):
    pass


# Properties to receive on update
class ItemUpdate(_BaseItem):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(_BaseItem):
    createdAt: Optional[_dt.datetime]
    itemId: int


# Properties to return to client
class Item(ItemInDBBase):
    pass


# Properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
