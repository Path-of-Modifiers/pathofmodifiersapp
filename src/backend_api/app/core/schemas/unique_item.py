import pydantic as _pydantic


# Shared modifier props
class UniqueItemBase(_pydantic.BaseModel):
    name: str
    itemBaseTypeId: int
    iconSuffix: str | None = None


# Properties to receive on modifier creation
class UniqueItemCreate(UniqueItemBase):
    pass


class UniqueItem(UniqueItemBase):
    uniqueItemId: int


class UniqueItemUpdate(UniqueItem):
    name: str | None = None
    itemBaseTypeId: int | None = None
