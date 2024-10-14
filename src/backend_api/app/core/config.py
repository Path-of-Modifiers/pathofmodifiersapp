import secrets
import warnings
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    EmailStr,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    API_V1_STR: str = "/api/api_v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    TURNSTILE_SECRET_KEY: str

    ACCESS_SESSION_EXPIRE_SECONDS: int = 60 * 60 * 24 * 1  # 1 day
    DOMAIN: str
    ENVIRONMENT: Literal["local", "staging", "production"] = "production"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    PROJECT_NAME: str = "Path of Modifiers"
    SENTRY_DSN: HttpUrl | None = None
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def ASYNC_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    REDIS_PORT: int = 6379
    REDIS_SERVER: str
    REDIS_CACHE: str = str(0)
    REDIS_PASSWORD: str = ""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def CACHE_URI(self) -> AnyUrl:
        return MultiHostUrl.build(
            scheme="redis",
            password=self.REDIS_PASSWORD,
            host=self.REDIS_SERVER,
            port=self.REDIS_PORT,
            path=self.REDIS_CACHE,
        )

    SMTP_TLS: bool = True
    SMTP_SSL: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None

    EMAILS_FROM_EMAIL: EmailStr | None = None
    EMAILS_FROM_NAME: EmailStr | None = None

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    EMAIL_RESET_TOKEN_EXPIRE_SECONDS: int = 60 * 10 * 1  # 10 minutes

    @computed_field  # type: ignore[prop-decorator]
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    TEST_USER_EMAIL: EmailStr = "test@example.com"
    TEST_USER_USERNAME: str = "testusername"
    TEST_DATABASE_URI: PostgresDsn | None = MultiHostUrl.build(
        scheme="postgresql+psycopg",
        username="test-pom-oltp-user",
        password="test-pom-oltp-password",
        host="test-db",
        port=5432,
        path="test-pom-oltp-db",
    )
    ASYNC_TEST_DATABASE_URI: PostgresDsn | None = MultiHostUrl.build(
        scheme="postgresql+asyncpg",
        username="test-pom-oltp-user",
        password="test-pom-oltp-password",
        host="test-db",
        port=5432,
        path="test-pom-oltp-db",
    )

    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_USERNAME: str
    FIRST_SUPERUSER_PASSWORD: str

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )
        self._check_default_secret("TURNSTILE_SECRET_KEY", self.TURNSTILE_SECRET_KEY)
        self._check_default_secret("REDIS_PASSWORD", self.REDIS_PASSWORD)
        self._check_default_secret("SMTP_PASSWORD", self.SMTP_PASSWORD)

        return self

    SKIP_RATE_LIMIT_TEST: bool = False

    # Rate limiting
    RATE_LIMIT: bool = False

    # Default user rate limits
    DEFAULT_USER_RATE_LIMIT_SECOND: str = "4/second"  # Default rate limit seconds
    DEFAULT_USER_RATE_LIMIT_MINUTE: str = "20/minute"  # Default rate limit minutes
    DEFAULT_USER_RATE_LIMIT_HOUR: str = "200/hour"  # Default rate limit hours
    DEFAULT_USER_RATE_LIMIT_DAY: str = "1000/day"  # Default rate limit days

    # Stricter default rate limits
    STRICT_DEFAULT_USER_RATE_LIMIT_SECOND: str = (
        "1/second"  # Default rate limit seconds
    )
    STRICT_DEFAULT_USER_RATE_LIMIT_MINUTE: str = (
        "1/minute"  # Default rate limit minutes
    )
    STRICT_DEFAULT_USER_RATE_LIMIT_HOUR: str = "3/hour"  # Default rate limit hours
    STRICT_DEFAULT_USER_RATE_LIMIT_DAY: str = "5/day"  # Default rate limit days

    # Login rate limits
    LOGIN_RATE_LIMIT_SECOND: str = "1/second"  # Default rate limit seconds
    LOGIN_RATE_LIMIT_MINUTE: str = "7/minute"  # Default rate limit minutes
    LOGIN_RATE_LIMIT_HOUR: str = "50/hour"  # Default rate limit hours
    LOGIN_RATE_LIMIT_DAY: str = "1000/day"  # Default rate limit days

    # Recovery password rate limits
    RECOVERY_PASSWORD_RATE_LIMIT_SECOND: str = "1/second"  # Default rate limit seconds
    RECOVERY_PASSWORD_RATE_LIMIT_MINUTE: str = "5/minute"  # Default rate limit minutes
    RECOVERY_PASSWORD_RATE_LIMIT_HOUR: str = "10/hour"  # Default rate limit hours
    RECOVERY_PASSWORD_RATE_LIMIT_DAY: str = "10/day"  # Default rate limit days

    # Reset password rate limits
    RESET_PASSWORD_RATE_LIMIT_SECOND: str = "1/second"  # Default rate limit seconds
    RESET_PASSWORD_RATE_LIMIT_MINUTE: str = "5/minute"  # Default rate limit minutes
    RESET_PASSWORD_RATE_LIMIT_HOUR: str = "10/hour"  # Default rate limit hours
    RESET_PASSWORD_RATE_LIMIT_DAY: str = "10/day"  # Default rate limit days

    # Update me rate limits
    UPDATE_ME_RATE_LIMIT_SECOND: str = "1/second"  # Default rate limit seconds
    UPDATE_ME_RATE_LIMIT_MINUTE: str = "1/minute"  # Default rate limit minutes
    UPDATE_ME_RATE_LIMIT_HOUR: str = "2/hour"  # Default rate limit hours
    UPDATE_ME_RATE_LIMIT_DAY: str = "2/day"  # Default rate limit days

    # Update password me rate limits
    UPDATE_PASSWORD_ME_RATE_LIMIT_SECOND: str = "1/second"  # Default rate limit seconds
    UPDATE_PASSWORD_ME_RATE_LIMIT_MINUTE: str = "1/minute"  # Default rate limit minutes
    UPDATE_PASSWORD_ME_RATE_LIMIT_HOUR: str = "3/hour"  # Default rate limit hours
    UPDATE_PASSWORD_ME_RATE_LIMIT_DAY: str = "5/day"  # Default rate limit days

    # Plotting rate limits
    PLOT_RATE_LIMIT_COOLDOWN_SECONDS: int = (
        30  # Cooldown amount for requests in seconds
    )
    TIER_SUPERUSER_PLOT_RATE_LIMIT: int = (
        30  # Superuser plots every PLOT_RATE_LIMIT_COOLDOWN_SECONDS
    )
    TIER_0_PLOT_RATE_LIMIT: int = (
        2  # Default plots every PLOT_RATE_LIMIT_COOLDOWN_SECONDS
    )
    TIER_1_PLOT_RATE_LIMIT: int = (
        3  # Default plots every PLOT_RATE_LIMIT_COOLDOWN_SECONDS
    )


settings = Settings()  # type: ignore
