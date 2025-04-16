from app.core.models.models import Currency as model_Currency
from app.core.models.models import Item as model_Item
from app.core.models.models import ItemBaseType as model_ItemBaseType
from app.core.models.models import ItemModifier as model_ItemModifier
from app.core.models.models import Modifier as model_Modifier
from app.core.models.models import UnidentifiedItem as model_UnidentifiedItem
from app.core.schemas.currency import Currency, CurrencyCreate, CurrencyUpdate
from app.core.schemas.item import Item, ItemCreate, ItemUpdate
from app.core.schemas.item_base_type import (
    ItemBaseType,
    ItemBaseTypeCreate,
    ItemBaseTypeUpdate,
)
from app.core.schemas.item_modifier import (
    ItemModifier,
    ItemModifierCreate,
    ItemModifierUpdate,
)
from app.core.schemas.modifier import Modifier, ModifierCreate
from app.core.schemas.unidentified_item import (
    UnidentifiedItem,
    UnidentifiedItemCreate,
    UnidentifiedItemUpdate,
)
from app.crud.extensions.crud_modifier import CRUDModifier
from app.crud.user import CRUDUser

from .base import CRUDBase

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

CRUD_unidentifiedItem = CRUDBase[
    model_UnidentifiedItem,
    UnidentifiedItem,
    UnidentifiedItemCreate,
    UnidentifiedItemUpdate,
](
    model=model_UnidentifiedItem,
    schema=UnidentifiedItem,
    create_schema=UnidentifiedItemCreate,
)

CRUD_modifier = CRUDModifier(
    model=model_Modifier,
    schema=Modifier,
    create_schema=ModifierCreate,
)

CRUD_user = CRUDUser()
