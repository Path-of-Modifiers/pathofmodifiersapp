from typing import Literal

from pydantic import BaseModel, Field


class FilterParams(BaseModel):
    limit: int | None = Field(None, gt=0)
    skip: int | None = Field(None, ge=0)
    sort_key: str | None = Field(None)
    sort_method: Literal["asc", "desc"] | None = Field(None)
