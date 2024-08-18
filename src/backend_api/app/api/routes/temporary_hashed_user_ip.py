from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.core.schemas as schemas
from app.api.deps import get_db
from app.api.utils import get_delete_return_message
from app.crud import CRUD_hashed_user_ip

router = APIRouter()


temporary_hashed_user_ip_prefix = "temporary_hashed_user_ip"


@router.post("/check/", response_model=bool)
async def check_temporary_hashed_user_ip(
    ip: str,
    db: Session = Depends(get_db),
):
    """
    Takes a query based on the 'TemporaryHashedUserIp' schema and retrieves
    whether the hashed user ip is valid.
    """

    is_valid = await CRUD_hashed_user_ip.check_temporary_hashed_ip(db, ip)

    return is_valid


@router.get(
    "/{temporaryHashedUserIp}",
    response_model=schemas.HashedUserIp | list[schemas.HashedUserIp],
)
async def get_temporary_hashed_user_ip(
    temporaryHashedUserIp: str,
    db: Session = Depends(get_db),
):
    """
    Get temporary hashed user ip by key and value for "temporaryHashedUserIp".
    """

    hashed_ip_map = {"hashedIp": temporaryHashedUserIp}
    hashed_ip = await CRUD_hashed_user_ip.get(db, filter=hashed_ip_map)

    return hashed_ip


@router.get("/", response_model=schemas.HashedUserIp | list[schemas.HashedUserIp])
async def get_all_temporary_hashed_user_ips(
    db: Session = Depends(get_db),
):
    """
    Get all temporary hashed user ips.
    """

    all_temporary_hashed_user_ips = await CRUD_hashed_user_ip.get(db)

    return all_temporary_hashed_user_ips


@router.post(
    "/",
    response_model=schemas.HashedUserIpCreate | list[schemas.HashedUserIpCreate],
)
async def create_temporary_hashed_user_ip(
    hashed_user_ip: schemas.HashedUserIpCreate | list[schemas.HashedUserIpCreate],
    db: Session = Depends(get_db),
):
    """
    Create temporary hashed user ip.
    """

    return await CRUD_hashed_user_ip.create(db=db, obj_in=hashed_user_ip)


@router.put(
    "/{temporaryHashedUserIp}",
    response_model=schemas.HashedUserIp | list[schemas.HashedUserIp],
)
async def update_temporary_hashed_user_ip(
    temporaryHashedUserIp: str,
    hashed_user_ip_update: schemas.HashedUserIpUpdate
    | list[schemas.HashedUserIpUpdate],
    db: Session = Depends(get_db),
):
    """
    Update temporary hashed user ip by key and value for "temporaryHashedUserIp".
    """

    hashed_ip_map = {"hashedIp": temporaryHashedUserIp}
    hashed_ip = await CRUD_hashed_user_ip.get(db, filter=hashed_ip_map)

    return await CRUD_hashed_user_ip.update(
        db_obj=hashed_ip, obj_in=hashed_user_ip_update, db=db
    )


@router.delete(
    "/{temporaryHashedUserIp}",
    response_model=str,
)
async def delete_temporary_hashed_user_ip(
    temporaryHashedUserIp: str,
    db: Session = Depends(get_db),
):
    """
    Delete temporary hashed user ip by key and value for "temporaryHashedUserIp".
    """

    hashed_ip_map = {"hashedIp": temporaryHashedUserIp}
    await CRUD_hashed_user_ip.remove(db, filter=hashed_ip_map)

    return get_delete_return_message(temporary_hashed_user_ip_prefix, hashed_ip_map)
