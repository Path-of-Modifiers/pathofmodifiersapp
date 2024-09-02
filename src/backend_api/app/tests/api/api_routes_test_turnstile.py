from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.api.api_message_util import get_failed_send_challenge_request_error_msg
from app.api.routes import turnstile_prefix
from app.core.config import settings
from app.tests.utils.utils import create_random_ip


@pytest.mark.usefixtures("clear_db", autouse=True)
class TestTurnstileRoutes:
    def test_success_turnstile_validation_always_passes(
        self, client: TestClient
    ) -> None:
        with patch(
            "app.core.config.settings.TURNSTILE_SECRET_KEY",
            "1x0000000000000000000000000000000AA",  # Always passes challenge
        ):
            data = {
                "token": "test_token",
                "ip": create_random_ip(),
            }
            response = client.post(
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

    def test_error_turnstile_validation_always_blocks(self, client: TestClient) -> None:
        with patch(
            "app.core.config.settings.TURNSTILE_SECRET_KEY",
            "2x0000000000000000000000000000000AA",  # Always blocks challenge
        ):
            data = {
                "token": "test_token",
                "ip": create_random_ip(),
            }
            response = client.post(
                f"{settings.API_V1_STR}/{turnstile_prefix}/", json=data
            )
            assert response.status_code == 400

            response_data = response.json()
            assert (
                response_data["detail"]
                == get_failed_send_challenge_request_error_msg(
                    ["invalid-input-response"]
                ).message
            )

    def test_error_turnstile_validation_token_already_spent(
        self, client: TestClient
    ) -> None:
        with patch(
            "app.core.config.settings.TURNSTILE_SECRET_KEY",
            "3x0000000000000000000000000000000AA",  # Invalid token
        ):
            data = {
                "token": "test_token",
                "ip": create_random_ip(),
            }
            response = client.post(
                f"{settings.API_V1_STR}/{turnstile_prefix}/", json=data
            )
            response_data = response.json()
            assert (
                response_data["detail"]
                == get_failed_send_challenge_request_error_msg(
                    ["timeout-or-duplicate"]
                ).message
            )
            assert response.status_code == 400

    def test_error_turnstile_validation_invalid_token(self, client: TestClient) -> None:
        with patch(
            "app.core.config.settings.TURNSTILE_SECRET_KEY",
            "IOIJIUSIUdfnnajdfnadnfkjnadnæhlk",  # Invalid token
        ):
            data = {
                "token": "test_token",
                "ip": create_random_ip(),
            }
            response = client.post(
                f"{settings.API_V1_STR}/{turnstile_prefix}/", json=data
            )
            response_data = response.json()
            assert (
                response_data["detail"]
                == get_failed_send_challenge_request_error_msg(
                    ["invalid-input-secret"]
                ).message
            )
            assert response.status_code == 400
