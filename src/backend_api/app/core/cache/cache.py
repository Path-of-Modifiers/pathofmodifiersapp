from redis.asyncio import Redis as AsyncRedis

from app.core.config import settings

cache = AsyncRedis.from_url(str(settings.CACHE_URI))
