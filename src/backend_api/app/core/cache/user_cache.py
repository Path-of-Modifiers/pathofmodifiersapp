from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import TypeAdapter

from app.core.cache.cache import cache
from app.core.models.models import User as model_User
from app.core.schemas.user import UserInCache
from app.exceptions.exceptions import InvalidTokenError


class UserCacheTokenType(StrEnum):
    SESSION = "instance_token"
    PASSWORD_RESET = "password_reset_token"
    REGISTER_USER = "register_user_token"


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

    def create_user_cache_instance(self, user: model_User, expire_seconds: int) -> UUID:
        """
        Creates a cache instance for the given user. Returns the access token.

        ``user`` is the user db object.
        ``expire_seconds`` is the number of seconds until the cache entry expires.
        """
        user_public = UserInCache(
            userId=user.userId,
            username=user.username,
            email=user.email,
            isActive=user.isActive,
            isSuperuser=user.isSuperuser,
            rateLimitTier=user.rateLimitTier,
            isBanned=user.isBanned,
        ).model_dump_json()

        access_token = uuid4()

        cache.set(
            name=f"user:{user.userId}:{self.user_token_type}:{access_token}",
            value=user_public,
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
        self, user: model_User, expire_seconds: int
    ) -> str:
        """
        Generate user confirmation token. The token will be sent to the user's email.
        """
        user_confirmation_identifier = self.create_user_cache_instance(
            user=user, expire_seconds=expire_seconds
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
                token=token,
            )

        token_user_data = user_cache_instances[0]

        if not token_user_data:
            raise InvalidTokenError(
                function_name=self.verify_token.__name__,
                token=token,
            )

        return token_user_data
