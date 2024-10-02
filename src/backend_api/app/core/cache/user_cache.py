from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from pydantic import TypeAdapter

from app.core.cache.cache import cache
from app.core.models.models import User as model_User
from app.core.schemas.user import UserInCache, UsernameStr
from app.exceptions import (
    InvalidCacheUpdateParamsError,
    InvalidTokenError,
)


class UserCacheTokenType(StrEnum):
    ACCESS_SESSION = "instance_token"
    PASSWORD_RESET = "password_reset_token"
    REGISTER_USER = "register_user_token"
    UPDATE_ME = "update_me_token"


user_cache_adapter = TypeAdapter(UserInCache)


class UserCache:
    """
    Some UserCache mechanics:

    The UUID or String `token` belongs to the client side.
    Format of `token` is  '*{username}:{cache_key}*'

    We need the username on the client side to use it in key_func on each request during rate limit,
    so the username is always in the headers of the request

    A subset string of `token` called `cache_key`, is stored as the key inside the cache.
    Format of `cache_key` is '*{user_token_type}:{token}*'

    We don't need username when storing the key inside the cache.
    """

    def __init__(self, user_token_type: UserCacheTokenType) -> None:
        self.user_token_type = user_token_type

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await cache.aclose()

    @staticmethod
    def extract_username_from_token(token: str) -> str:
        return token.split(":", 1)[0]

    def _create_cache_key_format(self, uuid_instance: UUID | str) -> str:
        return f"{self.user_token_type.value}:{uuid_instance}"

    def _create_token_format(
        self, username: UsernameStr, uuid_instance: UUID | str
    ) -> str:
        cache_key_format = self._create_cache_key_format(uuid_instance)
        return f"{username}:{cache_key_format}"

    def _extract_cache_key_from_token(self, token: str) -> str:
        return token.split(":", 1)[1]

    def _create_user_cache_by_user_model(
        self,
        user: model_User,
        *,
        update_params: dict[str, Any] | None = None,
    ) -> str:
        """
        Creates a cache instance for the given user. Returns a JSON representation of the model

        ``user`` is the user db object.
        ``update_params`` is the user update values.
        """
        user_in_cache = UserInCache(
            userId=user.userId,
            username=user.username,
            email=user.email,
            isActive=user.isActive,
            isSuperuser=user.isSuperuser,
            rateLimitTier=user.rateLimitTier,
            isBanned=user.isBanned,
        )

        if update_params:
            if (
                update_params.keys() - user_in_cache.__dict__.keys()
            ):  # Check if update_params has any keys that are not in user_in_cache
                raise InvalidCacheUpdateParamsError(
                    update_params=update_params,
                    object=user_in_cache,
                    function_name=self._create_user_cache_by_user_model.__name__,
                    class_name=self.__,
                )
            user_in_cache.__dict__.update(update_params)

        return user_in_cache.model_dump_json()

    async def _get_cache_instance_by_token(self, token: str) -> UserInCache | None:
        """Get user cache instance in cache"""
        cache_key = self._extract_cache_key_from_token(token)

        session_instance = await cache.get(cache_key)

        if session_instance:
            user_cache_instance = user_cache_adapter.validate_json(session_instance)
        else:
            user_cache_instance = None

        return user_cache_instance

    async def create_user_cache_instance(
        self,
        expire_seconds: int,
        user: model_User,
        *,
        update_params: dict[str, Any] | None = None,
    ) -> str:
        """
        Creates a cache instance for the given user. Returns the access token.

        ``user`` is the user db object.
        ``expire_seconds`` is the number of seconds until the cache entry expires.
        ``update_params`` is the user update values.
        """
        user_cache_model = self._create_user_cache_by_user_model(
            user, update_params=update_params
        )

        uuid_instance = uuid4()

        cache_key_format = self._create_cache_key_format(uuid_instance)

        await cache.set(
            name=cache_key_format,
            value=user_cache_model,
            ex=expire_seconds,
        )

        token = self._create_token_format(
            username=user.username, uuid_instance=uuid_instance
        )

        return token

    async def verify_token(
        self, token: str, updating_user: bool | None = None
    ) -> UserInCache | None:
        """
        Verify token and return the cached user.
        """
        try:
            user_cache_instance = await self._get_cache_instance_by_token(token)
        except Exception as e:
            raise InvalidTokenError(
                function_name=self.verify_token.__name__,
                class_name=self.__class__.__name__,
                token=token,
            ) from e

        if user_cache_instance is None:
            raise InvalidTokenError(
                function_name=self.verify_token.__name__,
                class_name=self.__class__.__name__,
                token=token,
            )

        username = UserCache.extract_username_from_token(token)

        # If someone is trying to manipulate with another username in token to bypass verification
        if not username == user_cache_instance.username and not updating_user:
            raise InvalidTokenError(
                function_name=self.verify_token.__name__,
                class_name=self.__class__.__name__,
                token=token,
            )

        return user_cache_instance
