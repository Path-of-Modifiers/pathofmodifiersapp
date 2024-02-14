from typing import List, Optional
from pydantic import PostgresDsn, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: Optional[PostgresDsn] = "postgresql://pom_oltp_superuser:sjukebarna123@localhost:5432/pom_oltp_db"

    model_config = SettingsConfigDict(env_prefix='POM_MODEL_')


settings = Settings()
