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

    def _scan_user_cache_instances(self, pattern: str) -> list[UserInCache]:
        # Initialize a list to hold the instance values
        user_cache_instances = []

        # Using SCAN to iterate through the keys
        cursor = "0"
        while cursor != 0:
            cursor, keys = cache.scan(cursor=cursor, match=pattern)
            # Retrieve all instance values for the keys found
            if keys:
                instances = cache.mget(keys)
                for instance in instances:
                    user_cache_instances.append(
                        user_cache_adapter.validate_json(instance)
                    )

        return user_cache_instances

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
                    class_name=self.__class__.__name__,
                )
            user_in_cache.__dict__.update(update_params)
        return user_in_cache.model_dump_json()

    def create_user_cache_instance(
        self,
        expire_seconds: int,
        user: model_User,
        *,
        update_params: dict[str, Any] | None = None,
    ) -> UUID:
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

        cache.set(
            name=f"user:{user.userId}:{self.user_token_type}:{access_token}",
            value=user_cache_model,
            ex=expire_seconds,
        )

        return access_token

    def get_user_cache_instances_by_token(
        self, token: UUID
    ) -> list[UserInCache] | None:
        """
        Gets all user cache instances for the given token.
        """
        # Pattern to match all instances for the given token
        pattern = f"user:*:{self.user_token_type}:{token}"

        user_cache_instances = self._scan_user_cache_instances(pattern)

        if not user_cache_instances:
            return None

        return user_cache_instances

    def get_user_cache_instances_by_user_id(
        self, user_id: UUID
    ) -> list[UserInCache] | None:
        """
        Gets all user cache instances for the given user id and user_token_type.
        """
        user_id_str = str(user_id)
        # Pattern to match all instances for the given userId
        pattern = f"user:{user_id_str}:{self.user_token_type}:*"

        user_cache_instances = self._scan_user_cache_instances(pattern)

        if not user_cache_instances:
            return None

        return user_cache_instances

    def generate_user_confirmation_token(
        self,
        user: model_User,
        expire_seconds: int,
        *,
        update_params: dict[str, Any] | None = None,
    ) -> str:
        """
        Generate user confirmation token. The token will be sent to the user's email.
        """
        user_confirmation_identifier = self.create_user_cache_instance(
            user=user, expire_seconds=expire_seconds, update_params=update_params
        )
        user_confirmation_token = str(user_confirmation_identifier)
        return user_confirmation_token

    def verify_token(self, token: str) -> UserInCache | None:
        """
        Verify token and return the cashed user.
        """
        # Just using the first instance. May need to change in the future
        user_cache_instances = self.get_user_cache_instances_by_token(token)

        if not user_cache_instances:
            raise InvalidTokenError(
                function_name=self.verify_token.__name__,
                class_name=self.__class__.__name__,
                token=token,
            )

        token_user_data = user_cache_instances[0]

        if not token_user_data:
            raise InvalidTokenError(
                token=token,
                function_name=self.verify_token.__name__,
                class_name=self.__class__.__name__,
            )

        return token_user_data
