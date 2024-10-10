from app.core.models.models import ItemBaseType as model_item_base_type
from app.core.schemas.item_base_type import (
    ItemBaseType,
    ItemBaseTypeCreate,
    ItemBaseTypeUpdate,
)
from app.crud.base import CRUDBase


class CRUDItemBaseType(
    CRUDBase[
        model_item_base_type,
        ItemBaseType,
        ItemBaseTypeCreate,
        ItemBaseTypeUpdate,
    ]
):
    pass
