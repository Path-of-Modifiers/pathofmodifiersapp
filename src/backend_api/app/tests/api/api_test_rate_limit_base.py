import asyncio
from collections.abc import Awaitable, Callable
from typing import Any
from unittest.mock import patch

from app.tests.base_test import BaseTest
from app.tests.utils.rate_limit import RateLimitPerTimeInterval


class TestRateLimitBase(BaseTest):
    """
    Base class for testing rate limit.
    """

    def _get_rate_and_interval(
        self, rate_limit_per_interval: RateLimitPerTimeInterval
    ) -> tuple[int, int]:
        """
        Get rate and interval from rate limit per interval type.
        """

        pattern = rate_limit_per_interval.rate_per_interval
        rate, interval = pattern.split("/")

        time_to_seconds = {"second": 1, "minute": 60, "hour": 3600, "day": 86400}

        return int(rate), time_to_seconds[interval]

    async def perform_time_interval_requests_with_api_function(
        self,
        api_function: Callable[[Any, Any], Awaitable[Any]],
        all_rate_limits_per_interval: (
            RateLimitPerTimeInterval | list[RateLimitPerTimeInterval]
        ),
        create_object_dict_func: Callable[[], dict[str, Any]] | None = None,
        **kwargs,
    ) -> None:
        """
        Performs rate limit test on `api_function` based on the rate limit per interval type.

        If `object_generator_func` is set, the api sends a request for each new dict created by it.
        """
        with patch("app.core.config.settings.RATE_LIMIT", True):
            if not isinstance(all_rate_limits_per_interval, list):
                all_rate_limits_per_interval = [all_rate_limits_per_interval]
            last_rate_limit_count = 0
            for rate_limits_per_interval in all_rate_limits_per_interval:
                rate, interval_seconds = self._get_rate_and_interval(
                    rate_limits_per_interval
                )
                if interval_seconds > 60:  # Skips test because it takes too long
                    continue
                skip_time = abs(rate - interval_seconds) // rate

                request_amount = rate - last_rate_limit_count
                for i in range(
                    request_amount + 2
                ):  # + 2 for guaranteeing getting 429 response
                    if create_object_dict_func is not None:
                        object_dict = create_object_dict_func()
                        response = await api_function(object_dict)
                    else:
                        response = await api_function(**kwargs)
                    assert response.status_code == 200 if i < request_amount else 429
                    await asyncio.sleep(skip_time)

                    # print(
                    #     f"{response.status_code} | {i} | {request_amount} | ResponseJson: {response.json()}"
                    # )
                    # if i >= request_amount:
                    #     print(
                    #         f"Rate limit reached, waiting for reset... response code: {response.status_code}",
                    #     )
                if response.status_code == 429:
                    await asyncio.sleep(
                        int(response.headers["Retry-After-Seconds"])
                    )  # Wait for rate to reset after seconds rate limit
                last_rate_limit_count = rate
