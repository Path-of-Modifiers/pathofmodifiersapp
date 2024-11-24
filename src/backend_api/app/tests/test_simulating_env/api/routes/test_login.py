from collections.abc import Awaitable

import pytest
from fastapi import Response
from httpx import AsyncClient

from app.api.routes.login import login_access_session, login_prefix
from app.core.config import settings
from app.tests.test_simulating_env.api.api_test_rate_limit_base import TestRateLimitBase
from app.tests.test_simulating_env.base_test import BaseTest
from app.tests.utils.rate_limit import (
    get_function_decorator_rate_limit_per_time_interval,
)


@pytest.mark.usefixtures("clear_db", autouse=True)
class TestLoginRoutes(BaseTest):
    @pytest.mark.anyio
    async def test_get_access_token_email(self, async_client: AsyncClient) -> None:
        login_data = {
            "username": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        }
        r = await async_client.post(
            f"{settings.API_V1_STR}/{login_prefix}/access-token", data=login_data
        )
        tokens = r.json()
        assert r.status_code == 200
        assert "access_token" in tokens
        assert tokens["access_token"]

    @pytest.mark.anyio
    async def test_get_access_token_username(self, async_client: AsyncClient) -> None:
        login_data = {
            "username": settings.FIRST_SUPERUSER_USERNAME,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        }
        r = await async_client.post(
            f"{settings.API_V1_STR}/login/access-token", data=login_data
        )
        tokens = r.json()
        assert r.status_code == 200
        assert "access_token" in tokens
        assert tokens["access_token"]

    @pytest.mark.anyio
    async def test_get_access_token_incorrect_password_email(
        self, async_client: AsyncClient
    ) -> None:
        login_data = {
            "username": settings.FIRST_SUPERUSER,
            "password": "incorrect",
        }
        r = await async_client.post(
            f"{settings.API_V1_STR}/{login_prefix}/access-token", data=login_data
        )
        assert r.status_code == 401

    @pytest.mark.anyio
    async def test_get_access_token_incorrect_password_user(
        self, async_client: AsyncClient
    ) -> None:
        login_data = {
            "username": settings.FIRST_SUPERUSER_USERNAME,
            "password": "incorrect",
        }
        r = await async_client.post(
            f"{settings.API_V1_STR}/login/access-token", data=login_data
        )
        assert r.status_code == 401


@pytest.mark.usefixtures("clear_db", autouse=True)
@pytest.mark.skipif(
    settings.SKIP_RATE_LIMIT_TEST is True or settings.SKIP_RATE_LIMIT_TEST == "True",
    reason="Rate limit test is disabled",
)
class TestLoginRateLimitAPI(TestRateLimitBase):
    @pytest.mark.anyio
    async def test_login_access_token_rate_limit(
        self,
        async_client: AsyncClient,
        ip_rate_limiter,  # noqa: ARG001 # Do not remove, used to enable ip rate limiter
    ) -> None:
        """
        Test login access token rate limit.
        """

        # Create api function to test
        def post_plot_query_from_api_normal_user(
            login_data: dict[str, str],
        ) -> Awaitable[Response]:
            return async_client.post(
                f"{settings.API_V1_STR}/{login_prefix}/access-token", data=login_data
            )

        # Get function decorator rate limit per time interval
        rate_limits_per_interval_format = (
            get_function_decorator_rate_limit_per_time_interval(login_access_session)
        )

        login_data = {
            "username": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        }

        await self.perform_time_interval_requests_with_api_function(
            api_function=post_plot_query_from_api_normal_user,
            all_rate_limits_per_interval=rate_limits_per_interval_format,
            login_data=login_data,
        )
