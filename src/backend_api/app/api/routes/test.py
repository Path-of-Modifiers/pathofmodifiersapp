from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.api.deps import (
    get_current_active_superuser,
    get_db,
)
from app.core.config import settings
from app.core.models.models import Item as model_Item
from app.core.models.models import User as model_User
from app.core.schemas import ItemCreate, User
from app.crud import CRUD_user
from app.logs.logger import test_logger as logger

router = APIRouter()


test_prefix = "test"


def bulk_insert_raw_sql(db: Session, count: int):
    """Generate dummy data for `count` objects"""
    data = [
        ItemCreate(
            stashId=f"Stash {i}",
            gameItemId=f"GameItem {i}",
            currencyId=1,
            baseType=f"Base {i}",
            ilvl=100,
            rarity="Rare",
            typeLine="Type {i}",
            league="Settlers",
            currencyAmount=100.0,
            valueInChaos=1.0,
            iconUrl="https://example.com/icon.png",
        )
        for i in range(count)
    ]

    # Prepare the raw SQL statement for bulk insert
    create_stmt = insert(model_Item)
    db.execute(create_stmt, data)

    # Execute the raw SQL with all accounts data
    db.commit()


@router.post(
    "/bulk-insert-test",
    dependencies=[
        Depends(get_current_active_superuser),  # Ensure only superusers can access
    ],
    response_model=dict,  # You can return a simple message here
)
async def bulk_insert_test(
    count: int,
    db: Session = Depends(get_db),
):
    """
    Test route for bulk inserting records.

    Returns a success message once the insertion is complete.
    """
    try:
        # Perform the bulk insert
        bulk_insert_raw_sql(db, count)
        return {"message": "Successfully bulk inserted data."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk insert failed: {str(e)}")


@router.post(
    "/bulk-insert-users-and-verify",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=dict,
)
async def bulk_insert_users_and_verify(count: int, db: Session = Depends(get_db)):
    """
    Test route for bulk inserting users and verifying them.

    Returns a success message once the insertion is complete.
    """
    logger.debug(f"Inserting {count} users")
    users_create = [
        User(
            username=str(i) + "testusername",
            email=str(i) + "testemail@me.com",
            isActive=True,
            isSuperuser=False,
            rateLimitTier=0,
            isBanned=False,
            userId=uuid4(),
            hashedPassword="$2a$12$vlTeiBOOnUKWx2kLCdpESejLnS7i8J84ijAy3.uOnCUpTSi7os0dm",  # Password is "testpassword"
            createdAt=None,
            updatedAt=None,
        )
        for i in range(count)
    ]

    filtered_users = [
        user
        for user in users_create
        if CRUD_user.get(db, filter={"email": user.email}) is None
    ]

    try:
        if not filtered_users:
            logger.debug("No users to insert")
        else:
            create_stmt = insert(model_User)
            db.execute(create_stmt, filtered_users)
            db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk insert failed: {str(e)}")

    logger.debug(f"Successfully inserted {count} users")

    logger.debug("Verifying users")

    # Verify users by making an internal request to the login route
    from app.main import app

    async with AsyncClient(
        app=app,
        base_url="http://localhost"
        + settings.API_V1_STR,  # Only to be used in localhost testing
    ) as client:
        for user in users_create:
            login_data = {
                "username": user.username,
                "password": "testpassword",  # The password used during creation
            }
            response = await client.post("/login/access-token", data=login_data)
            logger.debug("verify response: " + str(response.status_code))
            if response.status_code != 200:
                raise HTTPException(
                    status_code=500,
                    detail=f"User verification failed for {user.username}",
                )
            logger.debug(f"User {user.username} verified successfully.")

    return {"message": f"Successfully inserted and verified {count} users"}
