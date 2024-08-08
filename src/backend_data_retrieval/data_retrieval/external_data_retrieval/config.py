import os


class Settings:
    BASEURL: str = os.getenv("DOMAIN")
    MANUAL_NEXT_CHANGE_ID: bool = os.getenv("MANUAL_NEXT_CHANGE_ID") == "True"
    NEXT_CHANGE_ID: str = os.getenv("NEXT_CHANGE_ID")
    OATH_ACC_TOKEN_CONTACT_EMAIL: str = os.getenv("OATH_ACC_TOKEN_CONTACT_EMAIL")
    FIRST_SUPERUSER: str = os.getenv("FIRST_SUPERUSER")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD")
    CURRENT_SOFTCORE_LEAGUE: str = os.getenv("CURRENT_SOFTCORE_LEAGUE")
    POE_PUBLIC_STASHES_AUTH_TOKEN: str = os.getenv("POE_PUBLIC_STASHES_AUTH_TOKEN")
    OAUTH_CLIENT_ID: str = os.getenv("OAUTH_CLIENT_ID")
    OAUTH_CLIENT_SECRET: str = os.getenv("OAUTH_CLIENT_SECRET")
    OATH_ACC_TOKEN_CONTACT_EMAIL: str = os.getenv("OATH_ACC_TOKEN_CONTACT_EMAIL")


settings = Settings()
