# Rate limiting

from pydantic_settings import BaseSettings


class RateLimitSettings(BaseSettings):
    # Default IP rate limits
    DEFAULT_IP_RATE_LIMIT_SECOND: str = "14/second"
    DEFAULT_IP_RATE_LIMIT_MINUTE: str = "70/minute"
    DEFAULT_IP_RATE_LIMIT_HOUR: str = "250/hour"
    DEFAULT_IP_RATE_LIMIT_DAY: str = "1100/day"

    # Default user rate limits
    DEFAULT_USER_RATE_LIMIT_SECOND: str = "12/second"
    DEFAULT_USER_RATE_LIMIT_MINUTE: str = "60/minute"
    DEFAULT_USER_RATE_LIMIT_HOUR: str = "200/hour"
    DEFAULT_USER_RATE_LIMIT_DAY: str = "1000/day"

    # Stricter default rate limits
    STRICT_DEFAULT_USER_RATE_LIMIT_SECOND: str = "1/second"
    STRICT_DEFAULT_USER_RATE_LIMIT_MINUTE: str = "1/minute"
    STRICT_DEFAULT_USER_RATE_LIMIT_HOUR: str = "3/hour"
    STRICT_DEFAULT_USER_RATE_LIMIT_DAY: str = "5/day"

    # Login rate limits
    USER_LOGIN_RATE_LIMIT_SECOND: str = "1/second"
    USER_LOGIN_RATE_LIMIT_MINUTE: str = "8/minute"
    USER_LOGIN_RATE_LIMIT_HOUR: str = "50/hour"
    USER_LOGIN_RATE_LIMIT_DAY: str = "1000/day"
    IP_LOGIN_RATE_LIMIT_SECOND: str = "2/second"
    IP_LOGIN_RATE_LIMIT_MINUTE: str = "10/minute"
    IP_LOGIN_RATE_LIMIT_HOUR: str = "50/hour"
    IP_LOGIN_RATE_LIMIT_DAY: str = "1000/day"

    # Recovery password rate limits
    RECOVERY_PASSWORD_RATE_LIMIT_SECOND: str = "1/second"
    RECOVERY_PASSWORD_RATE_LIMIT_MINUTE: str = "5/minute"
    RECOVERY_PASSWORD_RATE_LIMIT_HOUR: str = "10/hour"
    RECOVERY_PASSWORD_RATE_LIMIT_DAY: str = "10/day"

    # Reset password rate limits
    RESET_PASSWORD_RATE_LIMIT_SECOND: str = "1/second"
    RESET_PASSWORD_RATE_LIMIT_MINUTE: str = "5/minute"
    RESET_PASSWORD_RATE_LIMIT_HOUR: str = "10/hour"
    RESET_PASSWORD_RATE_LIMIT_DAY: str = "10/day"

    # Update me rate limits
    UPDATE_ME_RATE_LIMIT_SECOND: str = "1/second"
    UPDATE_ME_RATE_LIMIT_MINUTE: str = "1/minute"
    UPDATE_ME_RATE_LIMIT_HOUR: str = "2/hour"
    UPDATE_ME_RATE_LIMIT_DAY: str = "3/day"
    # Used for updating username once a month
    UPDATE_ME_RATE_LIMIT_MONTH: str = "1/month"

    # Update password me rate limits
    UPDATE_PASSWORD_ME_RATE_LIMIT_SECOND: str = "1/second"
    UPDATE_PASSWORD_ME_RATE_LIMIT_MINUTE: str = "1/minute"
    UPDATE_PASSWORD_ME_RATE_LIMIT_HOUR: str = "3/hour"
    UPDATE_PASSWORD_ME_RATE_LIMIT_DAY: str = "5/day"

    # Plotting rate limits
    PLOT_RATE_LIMIT_IP_MAX_TRIES_PER_TIME_PERIOD: int = 5
    PLOT_RATE_LIMIT_COOLDOWN_SECONDS: int = 30
    TIER_SUPERUSER_PLOT_RATE_LIMIT: int = 30
    TIER_0_PLOT_RATE_LIMIT: int = 2
    TIER_1_PLOT_RATE_LIMIT: int = 3

    # Turnstile rate limits
    TURNSTILE_RATE_LIMIT_MAX_TRIES_PER_TIME_PERIOD: int = 4
    TURNSTILE_RATE_LIMIT_COOLDOWN_SECONDS: int = 1


rate_limit_settings = RateLimitSettings()  # type: ignore
