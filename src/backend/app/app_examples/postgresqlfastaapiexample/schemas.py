import datetime as _dt
import pydantic as _pydantic

class _BaseContact(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)

    name: str
    email: str
    phone: str


class Contact(_BaseContact):
    id: int
    created_at: _dt.datetime
    updated_at: _dt.datetime

    class Config:
        orm_mode = True

class CreateContact(_BaseContact):
    pass