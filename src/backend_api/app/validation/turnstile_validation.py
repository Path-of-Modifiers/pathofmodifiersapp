from fastapi import HTTPException
from pydantic import TypeAdapter
from requests import post

from app.api.api_message_util import get_failed_send_challenge_request_error_msg
from app.core.config import settings
from app.core.schemas import TurnstileQuery, TurnstileResponse


class ValidateTurnstileRequest:
    def __init__(self):
        self.validate = TypeAdapter(TurnstileResponse).validate_python
        self.turnstile_url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"

    async def validate_turnstile_request(
        self, *, request_data: TurnstileQuery
    ) -> TurnstileResponse:
        body = {
            "secret": settings.TURNSTILE_SECRET_KEY,
            "response": request_data.token,
            "remoteip": request_data.ip,
        }

        result = post(
            self.turnstile_url,
            json=body,
            headers={"Content-Type": "application/json"},
        )

        outcome = result.json()

        if result.status_code != 200:
            raise HTTPException(
                detail=get_failed_send_challenge_request_error_msg(
                    outcome["error-codes"]
                ).message,
                status_code=result.status_code,
            )

        if outcome["success"]:
            return self.validate(outcome)
        else:
            raise HTTPException(
                detail=get_failed_send_challenge_request_error_msg(
                    outcome["error-codes"]
                ).message,
                status_code=result.status_code,
            )
