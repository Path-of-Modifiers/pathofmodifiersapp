from typing import Annotated, Any, List, Optional
from pydantic import AnyUrl, BeforeValidator, PostgresDsn, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

import os
from typing_extensions import Self


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    API_V1_STR: str = "/api/api_v1"

    PROJECT_NAME: str = "Path of Modifiers"

    DATABASE_URL: Optional[PostgresDsn] = os.getenv("DATABASE_URL")

    model_config = SettingsConfigDict(env_prefix="POM_MODEL_")

    FIRST_SUPERUSER: str = os.getenv("FIRST_SUPERUSER")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD")

    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = (
        []
    )


settings = Settings()
