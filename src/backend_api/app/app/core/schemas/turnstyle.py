from typing import Annotated, List, Optional, Union
import pydantic as _pydantic
from pydantic import conlist


class TurnstyleQuery(_pydantic.BaseModel):
    token: str
    ip: str


class TurnstyleResponse(_pydantic.BaseModel):
    success: bool
    error_codes: Optional[List[str]] = None
    challenge_ts: str
    hostname: str
    action: str
    cdata: str
    metadata: dict
