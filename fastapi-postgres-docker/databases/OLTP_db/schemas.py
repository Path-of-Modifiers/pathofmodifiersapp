import datetime as _dt
from typing import Optional
import pydantic as _pydantic
from pydantic import Json

class _BaseCurrency(_pydantic.BaseModel):
    modelConfig = _pydantic.ConfigDict(fromAttributes=True)

    currencyName: str
    valueInChaos: float
    iconUrl: str

class Currency(_BaseCurrency):
    createdAt: Optional[_dt.datetime]
    updatedAt: Optional[_dt.datetime]

    class Config:
        ormMode = True

class CreateCurrency(_BaseCurrency):
    pass

class _BaseItem(_pydantic.BaseModel):
    modelConfig = _pydantic.ConfigDict(fromAttributes=True)

    itemId: str
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
    currencyName: Optional[str]
    corrupted: Optional[bool]
    delve: Optional[bool]
    fractured: Optional[bool]
    synthesized: Optional[bool]
    replica: Optional[bool]
    elder: Optional[bool]
    shaper: Optional[bool]
    influences: Optional[Json]
    searing: Optional[bool]
    tangled: Optional[bool]
    isrelic: Optional[bool]
    prefixes: Optional[int]
    suffixes: Optional[int]
    foilVariation: Optional[int]
    inventoryId: Optional[str]

class Item(_BaseItem):
    createdAt: Optional[_dt.datetime]
    updatedAt: Optional[_dt.datetime]

    class Config:
        ormMode = True

class CreateItem(_BaseItem):
    pass

class _BaseTransaction(_pydantic.BaseModel):
    modelConfig = _pydantic.ConfigDict(fromAttributes=True)

    itemId: str
    accountName: str
    currencyAmount: float
    currencyName: str

class Transaction(_BaseTransaction):
    transactionId: int
    createdAt: Optional[_dt.datetime]
    updatedAt: Optional[_dt.datetime]

    class Config:
        ormMode = True

class CreateTransaction(_BaseTransaction):
    pass

class _BaseItemBaseType(_pydantic.BaseModel):
    modelConfig = _pydantic.ConfigDict(fromAttributes=True)

    baseType: str
    category: str
    subCategory: Json

class ItemBaseType(_BaseItemBaseType):
    createdAt: Optional[_dt.datetime]
    updatedAt: Optional[_dt.datetime]

    class Config:
        ormMode = True

class CreateItemBaseType(_BaseItemBaseType):
    pass

class _BaseItemModifiers(_pydantic.BaseModel):
    modelConfig = _pydantic.ConfigDict(fromAttributes=True)

    modifierId: str
    itemId: str

class ItemModifiers(_BaseItemModifiers):
    pass

class CreateItemModifiers(_BaseItemModifiers):
    pass

class _BaseModifier(_pydantic.BaseModel):
    modelConfig = _pydantic.ConfigDict(fromAttributes=True)

    modifierId: str
    effect: str
    implicit: Optional[bool]
    explicit: Optional[bool]
    delve: Optional[bool]
    fractured: Optional[bool]
    synthesized: Optional[bool]
    corrupted: Optional[bool]
    enchanted: Optional[bool]
    veiled: Optional[bool]

class Modifier(_BaseModifier):
    createdAt: Optional[_dt.datetime]
    updatedAt: Optional[_dt.datetime]

    class Config:
        ormMode = True

class CreateModifier(_BaseModifier):
    pass

class _BaseModifierStats(_pydantic.BaseModel):
    modelConfig = _pydantic.ConfigDict(fromAttributes=True)

    modifierId: str
    statId: str

class ModifierStats(_BaseModifierStats):
    pass

class CreateModifierStats(_BaseModifierStats):
    pass

class _BaseStat(_pydantic.BaseModel):
    modelConfig = _pydantic.ConfigDict(fromAttributes=True)

    statId: str
    position: int
    statValue: int
    mininumValue: Optional[int]
    maximumValue: Optional[int]
    statTier: Optional[int]

class Stat(_BaseStat):
    createdAt: Optional[_dt.datetime]
    updatedAt: Optional[_dt.datetime]

    class Config:
        ormMode = True

class CreateStat(_BaseStat):
    pass

class _BaseStash(_pydantic.BaseModel):
    modelConfig = _pydantic.ConfigDict(fromAttributes=True)

    stashId: str
    accountName: str
    public: bool
    league: str

class Stash(_BaseStash):
    createdAt: Optional[_dt.datetime]
    updatedAt: Optional[_dt.datetime]

    class Config:
        ormMode = True

class CreateStash(_BaseStash):
    pass

class _BaseAccount(_pydantic.BaseModel):
    modelConfig = _pydantic.ConfigDict(fromAttributes=True)

    accountName: str
    isBanned: Optional[bool]

class Account(_BaseAccount):
    createdAt: Optional[_dt.datetime]
    updatedAt: Optional[_dt.datetime]

    class Config:
        ormMode = True

class CreateAccount(_BaseAccount):
    pass