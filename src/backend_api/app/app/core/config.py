from typing import List, Optional
from pydantic import PostgresDsn, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

import os

class Settings(BaseSettings):
    API_V1_STR: str = "/api/api_v1"
    
    PROJECT_NAME: str = "Path of Modifiers"

    DATABASE_URL: Optional[PostgresDsn] = (
        os.getenv("DATABASE_URL") 
    )

    model_config = SettingsConfigDict(env_prefix="POM_MODEL_")
    
    FIRST_SUPERUSER: str = os.getenv("FIRST_SUPERUSER")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD")


settings = Settings()
