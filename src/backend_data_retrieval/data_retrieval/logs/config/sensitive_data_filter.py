import re
from logging import Filter, LogRecord
from typing import Any


class SensitiveDataFilter(Filter):
    sensitive_patterns = [
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email addresses
        r"username",  # Matches 'username'
        r"user",  # Matches 'user'
        r"email",  # Matches 'email'
        r"password",  # Matches 'password'
        r"new_password",  # Matches 'new_password'
        r"token",  # Matches 'token'
        r"api_key",  # Matches 'api_key'
        r"secret",  # Matches 'secret'
        r"key",  # Matches 'key'
        r"access_token",  # Matches 'access_token'
        r"hashedPassword",  # Matches 'hashedPassword'
        r"passwordHash",  # Matches 'passwordHash'
        r"refresh_token",  # Matches 'refresh_token'
        r"auth_token",  # Matches 'auth token'
        r"oauth_token",  # Matches 'authorization token'
        r"SECRET_KEY",  # Matches 'SECRET_KEY'
        r"FIRST_SUPERUSER",  # Matches 'FIRST_SUPERUSER'
        r"FIRST_SUPERUSER_USERNAME",  # Matches 'FIRST_SUPERUSER_USERNAME'
        r"FIRST_SUPERUSER_PASSWORD",  # Matches 'FIRST_SUPERUSER_PASSWORD'
        r"POE_PUBLIC_STASHES_AUTH_TOKEN",  # Matches 'POE_PUBLIC_STASHES_AUTH_TOKEN'
        r"TURNSTILE_SECRET_KEY",  # Matches 'TURNSTILE_SECRET_KEY'
        r"SMTP_PASSWORD",  # Matches 'SMTP_PASSWORD'
        r"DATABASE_URL",  # Matches 'DATABASE_URL'
        r"PGADMIN_DEFAULT_PASSWORD",  # Matches 'PGADMIN_DEFAULT_PASSWORD'
        r"OATH_ACC_TOKEN_CONTACT_EMAIL",  # Matches 'OATH_ACC_TOKEN_CONTACT_EMAIL'
        r"OAUTH_CLIENT_SECRET",  # Matches 'OAUTH_CLIENT_SECRET'
        r"OAUTH_CLIENT_ID",  # Matches 'OAUTH_CLIENT_ID'
        r"REDIS_PASSWORD",  # Matches 'REDIS_PASSWORD'
    ]

    def _check_message_type(self, message: Any) -> str:
        if not isinstance(message, str):
            try:
                message = str(message)
            except Exception:
                message = "Message format not supported"
        return message

    def filter(self, record: LogRecord) -> bool:
        record.msg = self.mask_sensitive_data(record.msg)
        return True

    def mask_sensitive_data(self, message: Any):
        message = self._check_message_type(message)
        for pattern in self.sensitive_patterns:
            if re.search(pattern, message):
                message = "Details contains sensitive information."
        return message
