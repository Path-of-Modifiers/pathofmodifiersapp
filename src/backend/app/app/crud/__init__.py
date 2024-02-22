from .base import CRUDBase

from app.core.models.models import Currency

from app.core.schemas.account import AccountCreate, AccountUpdate, Account
from app.core.schemas.currency import CurrencyCreate, CurrencyUpdate, Currency
from app.core.schemas.item_base_type import ItemBaseTypeCreate, ItemBaseTypeUpdate, ItemBaseType
from app.core.schemas.item_modifier import ItemModifierCreate, ItemModifierUpdate, ItemModifier
from app.core.schemas.item import ItemCreate, ItemUpdate, Item
from app.core.schemas.modifier import ModifierCreate, ModifierUpdate, Modifier
from app.core.schemas.stash import StashCreate, StashUpdate, Stash


CRUD_account = CRUD_account = CRUDBase[
    Account,
    Account,
    AccountCreate,
    AccountUpdate,
](model=Account, schema=Account)


CRUD_currency = CRUD_currency = CRUDBase[
    Currency,
    Currency,
    CurrencyCreate,
    CurrencyUpdate,
](model=Currency, schema=Currency)


CRUD_itemBaseType = CRUD_itemBaseType = CRUDBase[
    ItemBaseType,
    ItemBaseType,
    ItemBaseTypeCreate,
    ItemBaseTypeUpdate,
](model=ItemBaseType, schema=ItemBaseType)


CRUD_itemModifier = CRUD_itemModifier = CRUDBase[
    ItemModifier,
    ItemModifier,
    ItemModifierCreate,
    ItemModifierUpdate,
](model=ItemModifier, schema=ItemModifier)

CRUD_item = CRUD_item = CRUDBase[
    Item,
    Item,
    ItemCreate,
    ItemUpdate,
](model=Item, schema=Item)

CRUD_modifier = CRUD_modifier = CRUDBase[
    Modifier,
    Modifier,
    ModifierCreate,
    ModifierUpdate,
](model=Modifier, schema=Modifier)

CRUD_stash = CRUD_stash = CRUDBase[
    Stash,
    Stash,
    StashCreate,
    StashUpdate,
](model=Stash, schema=Stash)

