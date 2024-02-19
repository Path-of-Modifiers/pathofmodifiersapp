import datetime as _dt
from typing import Optional
import pydantic as _pydantic
from pydantic import Json


# Shared item base type props
class _BaseItemBaseType(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    baseType: str
    category: str
    subCategory: Json


# Properties to receive on item base type creation
class CreateItemBaseType(_BaseItemBaseType):
    pass


# Properties to receive on update
class UpdateItemBaseType(_BaseItemBaseType):
    pass


# Properties shared by models stored in DB
class ItemBaseTypeInDBBase(_BaseItemBaseType):
    createdAt: Optional[_dt.datetime]
    updatedAt: Optional[_dt.datetime]
    id: int


# Properties to return to client
class ItemBaseType(ItemBaseTypeInDBBase):
    pass


# Properties stored in DB
class ItemBaseTypeInDB(ItemBaseTypeInDBBase):
    pass
