from collections.abc import Awaitable
from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
from fastapi import Response
from httpx import AsyncClient

from app.api.api_message_util import get_failed_send_challenge_request_error_msg
from app.api.routes import turnstile_prefix
from app.core.config import settings
from app.core.rate_limit.rate_limit_config import rate_limit_settings
from app.core.schemas.turnstile import TurnstileQuery
from app.tests.test_simulating_env.api.api_test_rate_limit_base import TestRateLimitBase
from app.tests.test_simulating_env.base_test import BaseTest
from app.tests.utils.rate_limit import RateLimitPerTimeInterval
from app.tests.utils.utils import create_random_ip


@pytest.mark.usefixtures("clear_db", autouse=True)
class TestTurnstileAPI(BaseTest):
    @pytest.mark.anyio
    async def test_success_turnstile_validation_always_passes(
        self, async_client: AsyncClient
    ) -> None:
        with patch(
            "app.core.config.settings.TURNSTILE_SECRET_KEY",
            "1x0000000000000000000000000000000AA",  # Always passes challenge
        ):
            data = {
                "token": "test_token",
                "ip": create_random_ip(),
            }
            response = await async_client.post(
                f"{settings.API_V1_STR}/{turnstile_prefix}/", json=data
            )
            response_data = response.json()
            assert response.status_code == 200
            assert response_data["success"] is True
            assert response_data["error_codes"] is None

            now = datetime.now()
            challenge_ts = datetime.strptime(
                response_data["challenge_ts"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            assert (
                now - challenge_ts < timedelta(seconds=300)
            )  # https://developers.cloudflare.com/turnstile/get-started/server-side-validation/

    @pytest.mark.anyio
    async def test_error_turnstile_validation_always_blocks(
        self, async_client: AsyncClient
    ) -> None:
        with patch(
            "app.core.config.settings.TURNSTILE_SECRET_KEY",
            "2x0000000000000000000000000000000AA",  # Always blocks challenge
        ):
            data = {
                "token": "test_token",
                "ip": create_random_ip(),
            }
            response = await async_client.post(
                f"{settings.API_V1_STR}/{turnstile_prefix}/", json=data
            )

            response_data = response.json()
            assert (
                response_data["detail"]
                == get_failed_send_challenge_request_error_msg(
                    e=["invalid-input-response"],
                ).message
            )

    @pytest.mark.anyio
    async def test_error_turnstile_validation_token_already_spent(
        self, async_client: AsyncClient
    ) -> None:
        with patch(
            "app.core.config.settings.TURNSTILE_SECRET_KEY",
            "3x0000000000000000000000000000000AA",  # Invalid token
        ):
            data = {
                "token": "test_token",
                "ip": create_random_ip(),
            }
            response = await async_client.post(
                f"{settings.API_V1_STR}/{turnstile_prefix}/", json=data
            )
            response_data = response.json()
            assert (
                response_data["detail"]
                == get_failed_send_challenge_request_error_msg(
                    e=["timeout-or-duplicate"],
                ).message
            )

    @pytest.mark.anyio
    async def test_error_turnstile_validation_invalid_token(
        self, async_client: AsyncClient
    ) -> None:
        with patch(
            "app.core.config.settings.TURNSTILE_SECRET_KEY",
            "IOIJIUSIUdfnnajdfnadnfkjnadnæhlk",  # Invalid token
        ):
            data = {
                "token": "test_token",
                "ip": create_random_ip(),
            }
            response = await async_client.post(
                f"{settings.API_V1_STR}/{turnstile_prefix}/", json=data
            )
            response_data = response.json()

            assert (
                response_data["detail"]
                == get_failed_send_challenge_request_error_msg(
                    e=["invalid-input-secret"],
                ).message
            )


@pytest.mark.usefixtures("clear_db", autouse=True)
@pytest.mark.skipif(
    settings.SKIP_RATE_LIMIT_TEST is True or settings.SKIP_RATE_LIMIT_TEST == "True",
    reason="Rate limit test is disabled",
)
class TestTurnstileRateLimitAPI(TestRateLimitBase):
    @pytest.mark.anyio
    async def test_post_turnstile_rate_limit(
        self,
        async_client: AsyncClient,
    ) -> None:
        """
        Perform rate limit test for POST plot endpoint.
        """
        with patch(
            "app.core.config.settings.TURNSTILE_SECRET_KEY",
            "1x0000000000000000000000000000000AA",  # Always passes challenge
        ):
            turnstile_query = {
                "token": "test_token",
                "ip": create_random_ip(),
            }

            async def post_turnstile_query_from_api_user(
                query: TurnstileQuery,
            ) -> Awaitable[Response]:
                return await async_client.post(
                    f"{settings.API_V1_STR}/{turnstile_prefix}/", json=query
                )

            # Get rate limit per time interval for POST plot request
            rate_limits_per_interval_format = RateLimitPerTimeInterval(
                rate_per_interval=f"{rate_limit_settings.TURNSTILE_RATE_LIMIT_MAX_TRIES_PER_TIME_PERIOD}/second"
            )

            await self.perform_time_interval_requests_with_api_function(
                api_function=post_turnstile_query_from_api_user,
                all_rate_limits_per_interval=rate_limits_per_interval_format,
                query=turnstile_query,
            )
