from typing import Any
from app.crud.base import CRUDBase

from app.core.schemas.modifier import ModifierCreate, ModifierUpdate, Modifier
from app.core.models.models import Modifier as model_Modifier
from sqlalchemy.orm import Session


class CRUDModifier(
    CRUDBase[
        model_Modifier,
        Modifier,
        ModifierCreate,
        ModifierUpdate,
    ]
):
    def __init__(self):
        pass
    
    
    def group_modifier_by_effect(self, db: Session, filter: Any = {}):
        db_obj = db.query(self.model).filter_by(**filter).all()