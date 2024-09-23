from collections.abc import Awaitable, Callable
from typing import Any

import pytest
from slowapi import Limiter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.tests.api.api_test_rate_limit_base import TestRateLimitBase
from app.tests.utils.rate_limit import RateLimitPerTimeInterval


@pytest.mark.usefixtures("clear_db", autouse=True)
@pytest.mark.usefixtures("clear_cache", autouse=True)
@pytest.mark.skipif(
    settings.SKIP_RATE_LIMIT_TEST is True or settings.SKIP_RATE_LIMIT_TEST == "True",
    reason="Rate limit test is disabled",
)
class TestRateLimitSlowAPI(TestRateLimitBase):
    """
    Class for testing slowapi rate limit.
    """

    @pytest.mark.anyio
    async def test_user_get_rate_limit(
        self,
        db: AsyncSession,
        get_object_from_api_normal_user: Callable[[Any, Any], Awaitable[Any]],
        get_request_all_rate_limits_per_interval: (
            RateLimitPerTimeInterval | list[RateLimitPerTimeInterval]
        ),
        object_generator_func: Callable[[], dict],
        user_rate_limiter: Limiter,  # noqa: ARG001 # Do not remove, used to enable user rate limiter
    ) -> None:
        """
        Tests rate limit with GET request. Uses user rate limiter.

        **Arguments**
        - `db`: DB session object
        - `get_object_from_api_normal_user`: API GET request function for getting object from API
        - `get_request_all_rate_limits_per_interval`: Rate limit per time interval for GET request
        - `object_generator_func`: Function for generating random object

        """

        _, object_out = await self._create_random_object_crud(db, object_generator_func)

        obj_out_pk_map = self._create_primary_key_map(object_out)
        await self.perform_time_interval_requests_with_api_function(
            api_function=get_object_from_api_normal_user,
            all_rate_limits_per_interval=get_request_all_rate_limits_per_interval,
            object_pk_map=obj_out_pk_map,
        )
