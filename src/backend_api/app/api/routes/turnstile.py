from fastapi import APIRouter, Request

import app.core.schemas as schemas
from app.api.deps import (
    get_user_ip_from_header,
)
from app.core.rate_limit.custom_rate_limiter import RateSpec
from app.core.rate_limit.rate_limit_config import rate_limit_settings
from app.core.rate_limit.rate_limiters import apply_custom_rate_limit
from app.validation import turnstile_validation_tool

router = APIRouter()


turnstile_prefix = "turnstile"


@router.post("/", response_model=schemas.TurnstileResponse)
async def get_turnstile_validation(
    request: Request,
    query: schemas.TurnstileQuery,
):
    """Takes a query based on the 'TurnstileQuery' schema and retrieves data
    based on the cloudfare challenge turnstile validation response.

    Args:
        query (schemas.TurnstileQuery): Query based on the 'TurnstileQuery' schema.
        verification (bool, optional): Verification flag. Defaults to Depends(verification).

    Raises:
        HTTPException: If verification fails.

    Returns:
        _type_: Returns a response based on the 'TurnstileResponse' schema.
    """
    rate_spec = RateSpec(
        requests=rate_limit_settings.TURNSTILE_RATE_LIMIT_MAX_TRIES_PER_TIME_PERIOD,
        cooldown_seconds=rate_limit_settings.TURNSTILE_RATE_LIMIT_COOLDOWN_SECONDS,
    )

    client_ip = get_user_ip_from_header(request)

    async with apply_custom_rate_limit(
        unique_key="turnstile_" + client_ip,
        rate_spec=rate_spec,
        prefix=turnstile_prefix,
    ):
        return await turnstile_validation_tool.validate_turnstile_request(
            request_data=query
        )
