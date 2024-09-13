from app.core.cache.user_cache import UserCache
from app.core.cache.user_cache import UserCacheTokenType

user_cache_session = UserCache(UserCacheTokenType.SESSION)
user_cache_password_reset = UserCache(UserCacheTokenType.PASSWORD_RESET)
user_cache_register_user = UserCache(UserCacheTokenType.REGISTER_USER)
user_cache_update_me = UserCache(UserCacheTokenType.UPDATE_ME)
