from redis import Redis

from app.core.config import settings

cache = Redis.from_url(str(settings.CACHE_URI))
