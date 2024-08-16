from typing import Annotated, List, Optional, Union
import pydantic as _pydantic
from pydantic import conlist


class TurnstileQuery(_pydantic.BaseModel):
    token: str
    ip: str

class MetadataObject(_pydantic.BaseModel):
    interactive: Optional[bool] = None

class TurnstileResponse(_pydantic.BaseModel):
    success: bool
    error_codes: Optional[List[str]] = None
    challenge_ts: Optional[str] = None
    hostname: Optional[str] = None
    action: Optional[str] = None
    cdata: Optional[str] = None
    metadata: Optional[MetadataObject] = None
