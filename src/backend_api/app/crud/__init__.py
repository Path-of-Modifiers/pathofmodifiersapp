from app.crud.user import CRUDUser
from .base import CRUDBase
from app.crud.extensions.crud_modifier import CRUDModifier

from app.core.models.models import Currency as model_Currency
from app.core.models.models import ItemBaseType as model_ItemBaseType
from app.core.models.models import ItemModifier as model_ItemModifier
from app.core.models.models import Modifier as model_Modifier
from app.core.models.models import Item as model_Item

from app.core.schemas.currency import CurrencyCreate, CurrencyUpdate, Currency
from app.core.schemas.item_base_type import (
    ItemBaseTypeCreate,
    ItemBaseType,
    ItemBaseTypeUpdate,
)
from app.core.schemas.item_modifier import (
    ItemModifierCreate,
    ItemModifierUpdate,
    ItemModifier,
)
from app.core.schemas.modifier import ModifierCreate, Modifier
from app.core.schemas.item import ItemCreate, ItemUpdate, Item

CRUD_currency = CRUDBase[
    model_Currency,
    Currency,
    CurrencyCreate,
    CurrencyUpdate,
](
    model=model_Currency,
    schema=Currency,
    create_schema=CurrencyCreate,
)


CRUD_itemBaseType = CRUDBase[
    model_ItemBaseType, ItemBaseType, ItemBaseTypeCreate, ItemBaseTypeUpdate
](model=model_ItemBaseType, schema=ItemBaseType, create_schema=ItemBaseTypeCreate)


CRUD_itemModifier = CRUDBase[
    model_ItemModifier,
    ItemModifier,
    ItemModifierCreate,
    ItemModifierUpdate,
](
    model=model_ItemModifier,
    schema=ItemModifier,
    create_schema=ItemModifierCreate,
)

CRUD_item = CRUDBase[
    model_Item,
    Item,
    ItemCreate,
    ItemUpdate,
](model=model_Item, schema=Item, create_schema=ItemCreate)

CRUD_modifier = CRUDModifier(
    model=model_Modifier,
    schema=Modifier,
    create_schema=ModifierCreate,
)

CRUD_user = CRUDUser()
