from app.core.models.models import Item as model_Item
from app.core.models.models import ItemAvailability as model_ItemAvailability
from app.core.models.models import ItemBaseType as model_ItemBaseType
from app.core.models.models import ItemModifier as model_ItemModifier
from app.core.schemas.item import Item, ItemCreate, ItemUpdate
from app.core.schemas.item_availability import (
    ItemAvailability,
    ItemAvailabilityCreate,
    ItemAvailabilityUpdate,
)
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
from app.crud.extensions.crud_currency import CRUDCurrency
from app.crud.extensions.crud_league import CRUDLeague
from app.crud.extensions.crud_modifier import CRUDModifier
from app.crud.extensions.crud_unidentifiedItem import CRUDUnidentifiedItem
from app.crud.user import CRUDUser

from .base import CRUDBase

CRUD_league = CRUDLeague()

CRUD_currency = CRUDCurrency()

CRUD_itemAvailability = CRUDBase[
    model_ItemAvailability,
    ItemAvailability,
    ItemAvailabilityCreate,
    ItemAvailabilityUpdate,
](
    model=model_ItemAvailability,
    schema=ItemAvailability,
    create_schema=ItemAvailabilityCreate,
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

CRUD_unidentifiedItem = CRUDUnidentifiedItem()

CRUD_modifier = CRUDModifier()

CRUD_user = CRUDUser()
