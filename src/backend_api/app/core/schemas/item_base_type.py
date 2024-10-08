import datetime as _dt

import pydantic as _pydantic


# Shared item base type props
class _BaseItemBaseType(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    baseType: str
    category: str
    subCategory: str | None = None


class BaseType(_pydantic.BaseModel):
    baseType: str


class ItemBaseTypeCategory(_pydantic.BaseModel):
    category: str


class ItemBaseTypeSubCategory(_pydantic.BaseModel):
    subCategory: str


# Properties to receive on item base type creation
class ItemBaseTypeCreate(_BaseItemBaseType):
    pass


# Properties to receive on update
class ItemBaseTypeUpdate(_BaseItemBaseType):
    pass


# Properties shared by models stored in DB
class ItemBaseTypeInDBBase(_BaseItemBaseType):
    pass


# Properties to return to client
class ItemBaseType(ItemBaseTypeInDBBase):
    pass


# Properties stored in DB
class ItemBaseTypeInDB(ItemBaseTypeInDBBase):
    pass
