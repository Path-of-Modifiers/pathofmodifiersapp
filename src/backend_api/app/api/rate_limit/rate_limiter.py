# From https://github.com/wemake-services/asyncio-redis-rate-limit
import asyncio
import hashlib
from types import TracebackType
from typing import NamedTuple, TypeAlias, TypeVar

from asyncio_redis_rate_limit.compat import (
    AnyPipeline,
    AnyRedis,
    pipeline_expire,
)
from typing_extensions import final

from app.exceptions.model_exceptions.plot_exception import PlotRateLimitExceededError

#: These aliases makes our code more readable.
_Seconds: TypeAlias = int

_RateLimiterT = TypeVar("_RateLimiterT", bound="RateLimiter")


@final
class RateLimitError(Exception):
    """We raise this error when rate limit is hit."""


@final
class RateSpec(NamedTuple):
    """
    Specifies the amount of requests can be made in the time frame in seconds.

    It is much nicier than using a custom string format like ``100/1s``.
    """

    requests: int
    seconds: _Seconds


class RateLimiter:
    """Implements rate limiting."""

    __slots__ = (
        "_unique_key",
        "_rate_spec",
        "_backend",
        "_cache_prefix",
        "_lock",
        "_enabled",
    )

    def __init__(
        self,
        unique_key: str,
        rate_spec: RateSpec,
        backend: AnyRedis,
        *,
        cache_prefix: str,
        enabled: bool = True,
    ) -> None:
        """In the future other backends might be supported as well."""
        self._unique_key = unique_key
        self._rate_spec = rate_spec
        self._backend = backend
        self._cache_prefix = cache_prefix
        self._lock = asyncio.Lock()
        self._enabled = enabled

    async def __aenter__(self: _RateLimiterT) -> _RateLimiterT:
        """
        Async context manager API.

        Before this object will be used, we call ``self._acquire`` to be sure
        that we can actually make any actions in this time frame.
        """
        if not self._enabled:
            return self
        await self._acquire()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Does nothing. We need this to ``__aenter__`` to work."""

    # Private API:

    async def _acquire(self) -> None:
        cache_key = self._make_cache_key(
            unique_key=self._unique_key,
            rate_spec=self._rate_spec,
            cache_prefix=self._cache_prefix,
        )
        pipeline = self._backend.pipeline()

        async with self._lock:
            current_rate = await self._run_pipeline(cache_key, pipeline)
            # This looks like a coverage error on 3.10:
            if current_rate > self._rate_spec.requests:  # pragma: no cover
                raise PlotRateLimitExceededError(
                    retry_after_seconds=self._rate_spec.seconds,
                    max_amount_of_tries_per_time_period=self._rate_spec.requests,
                    function_name=self._acquire.__name__,
                    class_name=self.__class__.__name__,
                )

    async def _run_pipeline(
        self,
        cache_key: str,
        pipeline: AnyPipeline,
    ) -> int:
        # https://redis.io/commands/incr/#pattern-rate-limiter-1
        current_rate, _ = await pipeline_expire(
            pipeline.incr(cache_key),
            cache_key,
            self._rate_spec.seconds,
        ).execute()
        return current_rate  # type: ignore[no-any-return]

    def _make_cache_key(
        self,
        unique_key: str,
        rate_spec: RateSpec,
        cache_prefix: str,
    ) -> str:
        parts = "".join([unique_key, str(rate_spec)])
        return (
            cache_prefix
            + hashlib.md5(  # noqa: S303, S324
                parts.encode("utf-8"),
            ).hexdigest()
        )
