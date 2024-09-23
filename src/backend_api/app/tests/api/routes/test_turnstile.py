from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
from httpx import AsyncClient

from app.api.api_message_util import get_failed_send_challenge_request_error_msg
from app.api.routes import turnstile_prefix
from app.core.config import settings
from app.tests.base_test import BaseTest
from app.tests.utils.utils import create_random_ip


@pytest.mark.usefixtures("clear_db", autouse=True)
class TestTurnstileAPI(BaseTest):
    async def test_success_turnstile_validation_always_passes(
        self, client: AsyncClient
    ) -> None:
        with patch(
            "app.core.config.settings.TURNSTILE_SECRET_KEY",
            "1x0000000000000000000000000000000AA",  # Always passes challenge
        ):
            data = {
                "token": "test_token",
                "ip": create_random_ip(),
            }
            response = await client.post(
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

    async def test_error_turnstile_validation_always_blocks(
        self, client: AsyncClient
    ) -> None:
        with patch(
            "app.core.config.settings.TURNSTILE_SECRET_KEY",
            "2x0000000000000000000000000000000AA",  # Always blocks challenge
        ):
            data = {
                "token": "test_token",
                "ip": create_random_ip(),
            }
            response = await client.post(
                f"{settings.API_V1_STR}/{turnstile_prefix}/", json=data
            )

            response_data = response.json()
            assert (
                response_data["detail"]
                == get_failed_send_challenge_request_error_msg(
                    e=["invalid-input-response"],
                ).message
            )

    async def test_error_turnstile_validation_token_already_spent(
        self, client: AsyncClient
    ) -> None:
        with patch(
            "app.core.config.settings.TURNSTILE_SECRET_KEY",
            "3x0000000000000000000000000000000AA",  # Invalid token
        ):
            data = {
                "token": "test_token",
                "ip": create_random_ip(),
            }
            response = await client.post(
                f"{settings.API_V1_STR}/{turnstile_prefix}/", json=data
            )
            response_data = response.json()
            assert (
                response_data["detail"]
                == get_failed_send_challenge_request_error_msg(
                    e=["timeout-or-duplicate"],
                ).message
            )

    async def test_error_turnstile_validation_invalid_token(
        self, client: AsyncClient
    ) -> None:
        with patch(
            "app.core.config.settings.TURNSTILE_SECRET_KEY",
            "IOIJIUSIUdfnnajdfnadnfkjnadnæhlk",  # Invalid token
        ):
            data = {
                "token": "test_token",
                "ip": create_random_ip(),
            }
            response = await client.post(
                f"{settings.API_V1_STR}/{turnstile_prefix}/", json=data
            )
            response_data = response.json()

            assert (
                response_data["detail"]
                == get_failed_send_challenge_request_error_msg(
                    e=["invalid-input-secret"],
                ).message
            )
