from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from pydantic import TypeAdapter

from app.core.cache.cache import cache
from app.core.models.models import User as model_User
from app.core.schemas.user import UserInCache
from app.exceptions import (
    InvalidCacheUpdateParamsError,
    InvalidTokenError,
)


class UserCacheTokenType(StrEnum):
    SESSION = "instance_token"
    PASSWORD_RESET = "password_reset_token"
    REGISTER_USER = "register_user_token"
    UPDATE_ME = "update_me_token"


user_cache_adapter = TypeAdapter(UserInCache)


class UserCache:
    def __init__(self, user_token_type: UserCacheTokenType) -> None:
        self.user_token_type = user_token_type

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await cache.aclose()

    def _create_key_format(self, token: UUID | str) -> str:
        """Format for how the key is stored in the cache"""
        return f"{self.user_token_type.value}:{token}"

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
        token_format = self._create_key_format(token)

        session_instance = await cache.get(token_format)

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

        access_token = uuid4()

        await cache.set(
            name=self._create_key_format(token=access_token),
            value=user_cache_model,
            ex=expire_seconds,
        )

        return str(access_token)

    async def verify_token(self, token: str) -> UserInCache | None:
        """
        Verify token and return the cached user.
        """
        user_cache_instance = await self._get_cache_instance_by_token(token)

        if user_cache_instance is None:
            raise InvalidTokenError(
                function_name=self.verify_token.__name__,
                class_name=self.__class__.__name__,
                token=token,
            )

        return user_cache_instance
