import datetime as _dt
from typing import Optional
import pydantic as _pydantic


class Influences(_pydantic.BaseModel):
    elder: Optional[bool] = None
    shaper: Optional[bool] = None
    crusader: Optional[bool] = None
    redeemer: Optional[bool] = None
    hunter: Optional[bool] = None
    warlord: Optional[bool] = None


# Shared item props
class _BaseItem(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    stashId: str
    gameItemId: str
    name: Optional[str] = None
    iconUrl: Optional[str] = None
    league: str
    typeLine: str
    baseType: str
    ilvl: int
    rarity: str
    identified: bool = True
    forumNote: Optional[str] = None
    currencyAmount: Optional[float] = None
    currencyId: Optional[int] = None
    corrupted: Optional[bool] = None
    delve: Optional[bool] = None
    fractured: Optional[bool] = None
    synthesized: Optional[bool] = None
    replica: Optional[bool] = None
    elder: Optional[bool] = None
    shaper: Optional[bool] = None
    influences: Optional[Influences] = None
    searing: Optional[bool] = None
    tangled: Optional[bool] = None
    isRelic: Optional[bool] = None
    prefixes: Optional[int] = None
    suffixes: Optional[int] = None
    foilVariation: Optional[int] = None


# Properties to receive on item creation
class ItemCreate(_BaseItem):
    pass


# Properties to receive on update
class ItemUpdate(_BaseItem):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(_BaseItem):
    createdAt: _dt.datetime
    itemId: int


# Properties to return to client
class Item(ItemInDBBase):
    pass


# Properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
