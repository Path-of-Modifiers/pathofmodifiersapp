from datetime import datetime

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    DOMAIN: str
    MANUAL_NEXT_CHANGE_ID: bool
    NEXT_CHANGE_ID: str
    OATH_ACC_TOKEN_CONTACT_EMAIL: str
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    CURRENT_SOFTCORE_LEAGUE: str
    POE_PUBLIC_STASHES_AUTH_TOKEN: str
    OAUTH_CLIENT_ID: str
    OAUTH_CLIENT_SECRET: str

    MINI_BATCH_SIZE: int = 30
    N_CHECKPOINTS_PER_TRANSFORMATION: int = 10

    LEAGUE_LAUNCH_TIME: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def LEAGUE_LAUNCH_DATETIME_OBJECT(self) -> datetime:
        return datetime.strptime(self.LEAGUE_LAUNCH_TIME, "%H-%d-%m-%Y")


settings = Settings()  # type: ignore
