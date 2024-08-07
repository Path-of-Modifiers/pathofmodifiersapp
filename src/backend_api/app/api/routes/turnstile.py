from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app.api.deps import get_db
from app.core.security import verification
from app.validation.turnstile_validation import validate_turnstile_request
import app.core.schemas as schemas


router = APIRouter()


turnstile_prefix = "turnstile"


@router.post("/", response_model=schemas.TurnstileResponse)
async def get_turnstile_validation(
    query: schemas.TurnstileQuery,
    verification: bool = Depends(verification),
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
    if not verification:
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorize API access for {get_turnstile_validation.__name__}",
        )

    return validate_turnstile_request(request_data=query)