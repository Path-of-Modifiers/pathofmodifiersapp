from app.core.cache.cache import cache


def clear_pom_cache():
    print("Clearing cache...")
    cache.flushall()
    print("Cache cleared successfully.")
