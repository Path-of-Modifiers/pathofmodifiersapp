import os
from pydantic import TypeAdapter
from requests import HTTPError, post

from app.core.schemas import TurnstileQuery, TurnstileResponse

TURNSTILE_SECRET_KEY = os.environ.get("TURNSTILE_SECRET_KEY")


def validate_turnstile_request(request_data: TurnstileQuery) -> TurnstileResponse:
    url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    body = {
        "secret": TURNSTILE_SECRET_KEY,
        "response": request_data.token,
        "remoteip": request_data.ip,
    }

    validate = TypeAdapter(TurnstileResponse).validate_python

    try:
        result = post(url, json=body, headers={"Content-Type": "application/json"})
    except Exception as e:
        raise HTTPError(
            f"""Failed to send challenge request to cloudflare turnstile
            endpoint with error: {e}"""
        )

    outcome = result.json()
    if outcome["success"]:
        return validate(outcome)
    else:
        raise HTTPError(
            f'Failed validation in turnstile request with error: {outcome["error-codes"]}'
        )
