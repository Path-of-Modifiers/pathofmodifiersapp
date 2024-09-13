from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import TypeAdapter

from app.core.cache.cache import cache
from app.core.models.models import User as model_User
from app.core.schemas.user import UserInCache
from app.exceptions import InvalidTokenError


class UserCacheTokenType(StrEnum):
    SESSION = "instance_token"
    PASSWORD_RESET = "password_reset_token"
    REGISTER_USER = "register_user_token"


user_cache_adapter = TypeAdapter(UserInCache)


class UserCache:
    def __init__(self, user_token_type: UserCacheTokenType) -> None:
        self.user_token_type = user_token_type

    def _create_key_format(self, token: UUID | str) -> str:
        """Format for how the key is stored in the cache"""
        return f"{self.user_token_type.value}:{token}"

    async def _get_cache_instance_by_token(self, token: str) -> UserInCache | None:
        """Get user cache instance in cache"""
        token_format = self._create_key_format(token)

        session_instance = await cache.get(token_format)
        await cache.aclose()

        if session_instance:
            session_instance = session_instance.decode("utf-8")
            user_cache_instance = user_cache_adapter.validate_json(session_instance)
        else:
            user_cache_instance = None

        return user_cache_instance

    async def create_user_cache_instance(
        self, user: model_User, expire_seconds: int
    ) -> UUID:
        """
        Creates a cache instance for the given user. Returns the access token.

        ``user`` is the user db object.
        ``expire_seconds`` is the number of seconds until the cache entry expires.
        """
        user_in_cache = UserInCache(
            userId=user.userId,
            username=user.username,
            email=user.email,
            isActive=user.isActive,
            isSuperuser=user.isSuperuser,
            rateLimitTier=user.rateLimitTier,
            isBanned=user.isBanned,
        ).model_dump_json()

        access_token = uuid4()

        await cache.set(
            name=self._create_key_format(token=access_token),
            value=user_in_cache,
            ex=expire_seconds,
        )
        await cache.aclose()

        return access_token

    async def generate_user_confirmation_token(
        self, user: model_User, expire_seconds: int
    ) -> str:
        """
        Generate user confirmation token. The token will be sent to the user's email.
        """
        user_confirmation_identifier = await self.create_user_cache_instance(
            user=user, expire_seconds=expire_seconds
        )
        return str(user_confirmation_identifier)

    async def verify_token(self, token: str) -> UserInCache | None:
        """
        Verify token and return the cached user.
        """
        user_cache_instance = await self._get_cache_instance_by_token(token)

        if not user_cache_instance or not isinstance(user_cache_instance, UserInCache):
            raise InvalidTokenError(
                function_name=self.verify_token.__name__,
                class_name=self.__class__.__name__,
                token=token,
            )

        return user_cache_instance
