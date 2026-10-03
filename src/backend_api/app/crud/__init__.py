from backend_api.app.core.models.models import ItemBaseType as model_ItemBaseType
from backend_api.app.core.schemas.item_base_type import (
    ItemBaseType,
    ItemBaseTypeCreate,
    ItemBaseTypeUpdate,
)
from backend_api.app.crud.extensions.crud_currency import CRUDCurrency
from backend_api.app.crud.extensions.crud_item import CRUDItem
from backend_api.app.crud.extensions.crud_league import CRUDLeague
from backend_api.app.crud.extensions.crud_modifier import CRUDModifier
from backend_api.app.crud.extensions.crud_unidentifiedItem import CRUDUnidentifiedItem
from backend_api.app.crud.user import CRUDUser

from .base import CRUDBase

CRUD_league = CRUDLeague()

CRUD_currency = CRUDCurrency()

CRUD_itemBaseType = CRUDBase[
    model_ItemBaseType, ItemBaseType, ItemBaseTypeCreate, ItemBaseTypeUpdate
](model=model_ItemBaseType, schema=ItemBaseType, create_schema=ItemBaseTypeCreate)

CRUD_item = CRUDItem()

CRUD_unidentifiedItem = CRUDUnidentifiedItem()

CRUD_modifier = CRUDModifier()

CRUD_user = CRUDUser()
