import redis.asyncio as Redis
from backend_api.app.core.config import settings

cache = Redis.from_url(str(settings.CACHE_URI), decode_responses=True)
