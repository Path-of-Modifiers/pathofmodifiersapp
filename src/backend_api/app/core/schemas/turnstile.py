import pydantic as _pydantic


class TurnstileQuery(_pydantic.BaseModel):
    token: str
    ip: str


class MetadataObject(_pydantic.BaseModel):
    interactive: bool | None = None


class TurnstileResponse(_pydantic.BaseModel):
    success: bool
    error_codes: list[str] | None = None
    challenge_ts: str | None = None
    hostname: str | None = None
    action: str | None = None
    cdata: str | None = None
    metadata: MetadataObject | None = None
