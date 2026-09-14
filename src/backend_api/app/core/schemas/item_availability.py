import pydantic as _pydantic


# Shared item props
class _BaseItemAvailability(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)
    itemId: int

    currencyId: int
    currencyAmount: float

    validFrom: int
    validTo: int | None = None

    isAsync: bool | None = None


# Properties to receive on item creation
class ItemAvailabilityCreate(_BaseItemAvailability):
    pass


# Properties to receive on update
class ItemAvailabilityUpdate(_BaseItemAvailability):
    pass


# Properties shared by models stored in DB
class ItemAvailabilityInDBBase(_BaseItemAvailability):
    availabilityId: int


# Properties to return to client
class ItemAvailability(ItemAvailabilityInDBBase):
    pass


# Properties stored in DB
class ItemAvailabilityInDB(ItemAvailabilityInDBBase):
    pass
