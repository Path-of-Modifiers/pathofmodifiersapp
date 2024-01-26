import datetime
from typing import Optional
from pydantic import BaseModel, Json


class Currency(BaseModel):

    currency_name: str
    value_in_chaos: float
    icon_url: str
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class Item(BaseModel):

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
    influences: Optional[Json]
    is_relic: Optional[bool]
    prefixes: Optional[int]
    suffixes: Optional[int]
    foil_variation: Optional[int]
    inventory_id: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class Transaction(BaseModel):

    transaction_id: int
    item_id: str
    account_name: str
    currency_amount: float
    currency_name: str
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class ItemCategories(BaseModel):

    category_name: str
    item_id: str


class ItemModifiers(BaseModel):

    modifier_id: str
    item_id: str


class Category(BaseModel):

    category_name: str
    is_sub_category: Optional[bool]


class Modifier(BaseModel):

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


class ModifierStats(BaseModel):

    modifier_id: str
    stat_id: str


class Stat(BaseModel):

    stat_id: str
    position: int
    stat_value: int
    mininum_value: Optional[int]
    maximum_value: Optional[int]
    stat_tier: Optional[int]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class Stash(BaseModel):

    stash_id: str
    account_name: str
    public: bool
    league: str
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class Account(BaseModel):

    account_name: str
    is_banned: Optional[bool]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
