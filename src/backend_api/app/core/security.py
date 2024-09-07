from enum import StrEnum
from uuid import UUID, uuid4

from passlib.context import CryptContext
from pydantic import TypeAdapter

from app.core.models.cache import cache
from app.core.models.models import User as model_User
from app.core.schemas.user import UserInCache

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCacheRole(StrEnum):
    SESSION = "session"
    PASSWORD_RESET = "password_reset"


user_cache_adapter = TypeAdapter(UserInCache)


class UserCache:
    def __init__(self, role: UserCacheRole) -> None:
        self.role = role

    def _scan_user_cache_instances(self, pattern: str) -> list[UserInCache]:
        # Initialize a list to hold the session values
        user_cache_instances = []

        # Using SCAN to iterate through the keys
        cursor = "0"
        while cursor != 0:
            cursor, keys = cache.scan(cursor=cursor, match=pattern)
            # Retrieve all session values for the keys found
            if keys:
                sessions = cache.mget(keys)
                for session in sessions:
                    user_cache_instances.append(
                        user_cache_adapter.validate_json(session)
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
            name=f"user:{user.userId}:{self.role}:{access_token}",
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
        # Pattern to match all sessions for the given token
        pattern = f"user:*:{self.role}:{token}"

        user_cache_instances = self._scan_user_cache_instances(pattern)

        if not user_cache_instances:
            return None

        return user_cache_instances

    def get_user_cache_instances_by_user_id(
        self, user_id: UUID
    ) -> list[UserInCache] | None:
        """
        Gets all user cache instances for the given user id and role.
        """
        user_id_str = str(user_id)
        # Pattern to match all sessions for the given userId
        pattern = f"user:{user_id_str}:{self.role}:*"

        user_cache_instances = self._scan_user_cache_instances(pattern)

        if not user_cache_instances:
            return None

        return user_cache_instances


user_cache_session = UserCache(UserCacheRole.SESSION)
user_cache_password_reset = UserCache(UserCacheRole.PASSWORD_RESET)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
