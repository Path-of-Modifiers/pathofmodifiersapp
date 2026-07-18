from contextlib import contextmanager

import redis

from data_retrieval_app.external_data_retrieval.config import settings


@contextmanager
def get_cache():
    cache = redis.from_url(str(settings.CACHE_URI), decode_responses=True)

    try:
        yield cache
    finally:
        cache.close()
