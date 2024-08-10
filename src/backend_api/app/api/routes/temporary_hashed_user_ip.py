from __future__ import annotations
from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app.api.deps import get_db
from app.core.security import verification
import app.core.schemas as schemas

from app.validation import hashed_ip_validation_tool

router = APIRouter()


modifier_prefix = "temporary_hashed_ip"


@router.post("/", response_model=schemas.HashedUserIp)
async def check_temporary_hashed_user_ip(
    query: schemas.HashedUserIpQuery,
    db: Session = Depends(get_db),
    validation: bool = Depends(verification),
):
    """
    Takes a query based on the 'TemporaryHashedUserIp' schema and retrieves
    whether the hashed user ip is valid.
    """
    if not validation:
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorize API access for {check_temporary_hashed_user_ip.__name__}",
        )

    return await hashed_ip_validation_tool.check_temporary_hashed_ip(
        db, request_data=query.hashedIp
    )


@router.get("/", response_model=Union[schemas.HashedUserIp, List[schemas.HashedUserIp]])
async def get_all_temporary_hashed_user_ips(
    db: Session = Depends(get_db), validation: bool = Depends(verification)
):
    """
    Get all temporary hashed user ips.
    """
    if not validation:
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorize API access for {get_all_temporary_hashed_user_ips.__name__}",
        )

    return await hashed_ip_validation_tool.get_all_temporary_hashed_user_ips(db)
