from redis import Redis

from app.core.config import settings

cache = Redis(
    host="my-redis.cloud.redislabs.com",
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,  # use your Redis password
    ssl=True,
    ssl_certfile="./redis_user.crt",
    ssl_keyfile="./redis_user_private.key",
    ssl_ca_certs="./redis_ca.pem",
)
