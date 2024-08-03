from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app.api.deps import get_db
from app.core.security import verification
from app.validation.turnstyle_validation import validate_turnstyle_request
import app.core.schemas as schemas


router = APIRouter()


turnstyle_prefix = "turnstyle"


@router.post("/", response_model=schemas.TurnstyleResponse)
async def get_turnstyle_validation(
    query: schemas.TurnstyleQuery,
    verification: bool = Depends(verification),
):
    """Takes a query based on the 'TurnstyleQuery' schema and retrieves data
    based on the cloudfare challenge turnstyle validation response.

    Args:
        query (schemas.TurnstyleQuery): Query based on the 'TurnstyleQuery' schema.
        verification (bool, optional): Verification flag. Defaults to Depends(verification).

    Raises:
        HTTPException: If verification fails.

    Returns:
        _type_: Returns a response based on the 'TurnstyleResponse' schema.
    """
    if not verification:
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorize API access for {get_turnstyle_validation.__name__}",
        )

    return await validate_turnstyle_request(query=query)
