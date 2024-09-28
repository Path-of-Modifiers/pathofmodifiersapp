import asyncio
import time
from collections.abc import Awaitable
from logging import Logger
from typing import Any

import pytest
from fastapi import Response
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.api.routes.plot import plot_prefix
from app.core.config import settings
from app.tests.api.api_test_rate_limit_base import TestRateLimitBase
from app.tests.utils.model_utils.plot import create_minimal_random_plot_query_dict
from app.tests.utils.rate_limit import RateLimitPerTimeInterval


@pytest.mark.usefixtures("clear_cache", autouse=True)
class TestPlotAPI(TestRateLimitBase):
    @pytest.mark.anyio
    async def test_post_multiple_plots_with_different_users(
        self,
        db: Session,
        async_client: AsyncClient,
        multiple_async_normal_user_token_headers: list[dict[str, str]],
        test_logger: Logger,
        async_db: AsyncSession,  # noqa: ARG001
    ) -> None:
        """
        Perform multiple POST requests with different users in parallel.
        """
        await asyncio.sleep(0.5)
        plot_query = await create_minimal_random_plot_query_dict(db)

        loop_time = time.time()
        # Create API function for POST plot request
        responses = []
        for i in range(len(multiple_async_normal_user_token_headers)):
            response = async_client.post(
                f"{settings.API_V1_STR}/{plot_prefix}/",
                headers=multiple_async_normal_user_token_headers[i],
                json=plot_query,
            )
            responses.append(response)

        responses = await asyncio.gather(*responses)

        for response in responses:
            assert response.status_code == 200

        total_time = time.time() - loop_time
        test_logger.info(
            f"Total time used on plotting with {len(multiple_async_normal_user_token_headers)} users: {total_time}"
        )


@pytest.mark.usefixtures("clear_cache", autouse=True)
@pytest.mark.skipif(
    settings.SKIP_RATE_LIMIT_TEST is True or settings.SKIP_RATE_LIMIT_TEST == "True",
    reason="Rate limit test is disabled",
)
class TestPlotRateLimitAPI(TestRateLimitBase):
    @pytest.mark.anyio
    async def test_post_plot_rate_limit(
        self,
        db: Session,
        async_client: AsyncClient,
        superuser_token_headers: dict[str, str],
        async_db: AsyncSession,  # noqa: ARG001
    ) -> None:
        """
        Perform rate limit test for POST plot endpoint.
        """
        plot_query = await create_minimal_random_plot_query_dict(db)

        # Create API function for POST plot request
        async def post_plot_query_from_api_super_user(
            query: dict[str, Any],
        ) -> Awaitable[Response]:
            return await async_client.post(
                f"{settings.API_V1_STR}/{plot_prefix}/",
                headers=superuser_token_headers,
                json=query,
            )

        # Get rate limit per time interval for POST plot request
        rate_limits_per_interval_format = RateLimitPerTimeInterval(
            rate_per_interval=f"{settings.TIER_SUPERUSER_PLOT_RATE_LIMIT}/second"
        )

        await self.perform_time_interval_requests_with_api_function(
            api_function=post_plot_query_from_api_super_user,
            all_rate_limits_per_interval=rate_limits_per_interval_format,
            query=plot_query,
        )
