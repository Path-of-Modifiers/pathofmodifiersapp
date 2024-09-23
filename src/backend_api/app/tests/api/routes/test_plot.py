from collections.abc import Awaitable
from typing import Any

import pytest
from fastapi import Response
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app.api.routes.plot import plot_prefix
from app.core.config import settings
from app.tests.api.api_test_rate_limit_base import TestRateLimitBase
from app.tests.utils.model_utils.plot import create_minimal_random_plot_query_dict
from app.tests.utils.rate_limit import RateLimitPerTimeInterval


@pytest.mark.usefixtures("clear_db", autouse=True)
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
        client: AsyncClient,
        normal_user_token_headers: dict[str, str],
    ) -> None:
        """
        Perform rate limit test for POST plot endpoint.
        """
        plot_query = await create_minimal_random_plot_query_dict(db)

        # Create API function for POST plot request
        def post_plot_query_from_api_normal_user(
            query: dict[str, Any],
        ) -> Awaitable[Response]:
            return client.post(
                f"{settings.API_V1_STR}/{plot_prefix}/",
                headers=normal_user_token_headers,
                json=query,
            )

        # Get rate limit per time interval for POST plot request
        rate_limits_per_interval_format = RateLimitPerTimeInterval(
            rate_per_interval=f"{settings.TIER_0_PLOT_RATE_LIMIT}/second"
        )

        await self.perform_time_interval_requests_with_api_function(
            api_function=post_plot_query_from_api_normal_user,
            all_rate_limits_per_interval=rate_limits_per_interval_format,
            query=plot_query,
        )
