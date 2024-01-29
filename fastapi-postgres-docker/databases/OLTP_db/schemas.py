import datetime
from typing import Optional, Json
import pydantic as _pydantic


class _BaseCurrency(_pydantic.BaseModel):

    currency_name: str
    value_in_chaos: float
    icon_url: str


class Currency(_BaseCurrency):

    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True

class CreateCurrency(_BaseCurrency):
    pass
        

class _BaseItem(_pydantic.BaseModel):
    
    item_id: str
    stash_id: str
    name: Optional[str]
    icon_url: Optional[str]
    league: str
    base_type: str
    type_line: str
    rarity: str
    identified: bool
    item_level: int
    forum_note: Optional[str]
    currency_amount: Optional[float]
    currency_name: Optional[str]
    corrupted: Optional[bool]
    delve: Optional[bool]
    fractured: Optional[bool]
    synthesized: Optional[bool]
    replica: Optional[bool]
    elder: Optional[bool]
    shaper: Optional[bool]
    searing: Optional[bool]
    tangled: Optional[bool]
    influences: Optional[_pydantic.Json]
    is_relic: Optional[bool]
    prefixes: Optional[int]
    suffixes: Optional[int]
    foil_variation: Optional[int]
    inventory_id: Optional[str]


class Item(_BaseItem):
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True


class CreateItem(_BaseItem):
    pass


class _BaseTransaction(_pydantic.BaseModel):
    item_id: str
    account_name: str
    currency_amount: float
    currency_name: str


class Transaction(_BaseTransaction):
    transaction_id: int
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True


class CreateTransaction(_BaseTransaction):
    pass


class ItemCategories(_pydantic.BaseModel):

    category_name: str
    item_id: str


class ItemModifiers(_pydantic.BaseModel):

    modifier_id: str
    item_id: str


class Category(_pydantic.BaseModel):

    category_name: str
    is_sub_category: Optional[bool]


class Modifier(_pydantic.BaseModel):

    modifier_id: str
    effect: str
    implicit: Optional[bool]
    explicit: Optional[bool]
    delve: Optional[bool]
    fractured: Optional[bool]
    synthesized: Optional[bool]
    corrupted: Optional[bool]
    enchanted: Optional[bool]
    veiled: Optional[bool]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class ModifierStats(_pydantic.BaseModel):

    modifier_id: str
    stat_id: str


class Stat(_pydantic.BaseModel):

    stat_id: str
    position: int
    stat_value: int
    mininum_value: Optional[int]
    maximum_value: Optional[int]
    stat_tier: Optional[int]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class Stash(_pydantic.BaseModel):

    stash_id: str
    account_name: str
    public: bool
    league: str
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class Account(_pydantic.BaseModel):

    account_name: str
    is_banned: Optional[bool]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
