from typing import List
import pydantic as _pydantic


class TurnstyleQuery(_pydantic.BaseModel):
    token: str
    ip: str


class TurnstyleResponse(_pydantic.BaseModel):
    success: bool
    challenge_ts: str
    hostname: str
    error_codes: List[str]
