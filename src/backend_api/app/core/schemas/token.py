from pydantic import BaseModel, Field


# JSON payload containing access token
class Token(BaseModel):
    access_token: str


# Contents of JWT token
class TokenPayload(BaseModel):
    sub: str | None = None


class NewPassword(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


class RecoverPassword(BaseModel):
    username: str | None = None
    email: str | None = None
