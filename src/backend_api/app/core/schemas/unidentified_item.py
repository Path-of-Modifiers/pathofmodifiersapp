import pydantic as _pydantic


# Shared item props
class _BaseUnidentifiedItem(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    name: str | None = None
    league: str
    itemBaseTypeId: int
    ilvl: int
    rarity: str
    identified: bool = False
    currencyAmount: float | None = None
    currencyId: int | None = None


# Properties to receive on item creation
class UnidentifiedItemCreate(_BaseUnidentifiedItem):
    createdHoursSinceLaunch: int


# Properties to receive on update
class UnidentifiedItemUpdate(_BaseUnidentifiedItem):
    pass


# Properties shared by models stored in DB
class UnidentifiedItemInDBBase(_BaseUnidentifiedItem):
    createdHoursSinceLaunch: int
    itemId: int
    nItems: int
    aggregated: bool


# Properties to return to client
class UnidentifiedItem(UnidentifiedItemInDBBase):
    pass


# Properties stored in DB
class UnidentifiedItemInDB(UnidentifiedItemInDBBase):
    pass
