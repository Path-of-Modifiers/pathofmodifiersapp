from __future__ import annotations

from fastapi import APIRouter

import app.core.schemas as schemas
from app.validation import turnstile_validation_tool

router = APIRouter()


turnstile_prefix = "turnstile"


@router.post("/", response_model=schemas.TurnstileResponse)
async def get_turnstile_validation(
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

    return await turnstile_validation_tool.validate_turnstile_request(
        request_data=query
    )
