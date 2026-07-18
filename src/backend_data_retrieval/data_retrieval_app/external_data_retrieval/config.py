from pydantic import (
    HttpUrl,
    computed_field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    DOMAIN: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def BACKEND_BASE_URL(self) -> HttpUrl:
        if "localhost" not in self.DOMAIN:
            return HttpUrl(f"https://{self.DOMAIN}/api/api_v1")
        else:
            return HttpUrl("http://src-backend-1:8000/api/api_v1")

    MANUAL_NEXT_CHANGE_ID: bool
    NEXT_CHANGE_ID: str
    OATH_ACC_TOKEN_CONTACT_EMAIL: str
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str

    POE_PUBLIC_STASHES_AUTH_TOKEN: str
    OAUTH_CLIENT_ID: str
    OAUTH_CLIENT_SECRET: str

    MINI_BATCH_SIZE: int = 30
    N_CHECKPOINTS_PER_TRANSFORMATION: int = 10

    MAX_TIME_PER_MINI_BATCH: int = 3 * 60


settings = Settings()  # type: ignore
