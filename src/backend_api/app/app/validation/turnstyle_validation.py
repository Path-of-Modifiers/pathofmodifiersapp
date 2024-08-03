import os
from pydantic import TypeAdapter
from requests import HTTPError, post

from app.core.schemas import TurnstyleQuery, TurnstyleResponse

TURNSTILE_SECRET_KEY = os.environ.get("TURNSTILE_SECRET_KEY")


def validate_turnstyle_request(request_data: TurnstyleQuery) -> TurnstyleResponse:
    url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    body = {
        "secret": TURNSTILE_SECRET_KEY,
        "response": request_data.token,
        "remoteip": request_data.ip,
    }

    validate = TypeAdapter(TurnstyleResponse).validate_python

    try:
        result = post(url, json=body, headers={"Content-Type": "application/json"})
        print("result", result)
    except Exception as e:
        raise HTTPError(
            f"""Failed to send challenge request to cloudflare turnstyle
            endpoint with error: {e}"""
        )

    outcome = result.json()
    print("outcome", outcome)
    if outcome["success"]:
        return validate(outcome)
    else:
        raise HTTPError(
            f'Failed validation in turnstyle request with error: {outcome["error-codes"]}'
        )
