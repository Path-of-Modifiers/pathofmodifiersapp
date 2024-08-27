from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings

# Create a limiter instance
limiter = Limiter(
    key_func=lambda: get_remote_address(),  # Limits based on IP address is default, but can be changed to other functions
    storage_uri=str(settings.CACHE_URI),
    default_limits=["10/minute"],
)
