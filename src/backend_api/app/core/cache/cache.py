import redis.asyncio as Redis

from app.core.config import settings

cache = Redis.from_url(str(settings.CACHE_URI), decode_responses=True)
