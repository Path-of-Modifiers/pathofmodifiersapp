from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from httpx import ASGITransport, AsyncClient
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
from app.exceptions.model_exceptions.test_exception import OnlyAvailableInLocalEnvError
from app.logs.logger import test_logger as logger

router = APIRouter()


test_prefix = "test"


def bulk_insert_raw_sql(db: Session, count: int):
    """Generate dummy data for `count` objects"""
    data = [
        ItemCreate(
            currencyId=1,
            baseType=f"Base {i}",
            ilvl=100,
            rarity="Rare",
            typeLine="Type {i}",
            league="Settlers",
            currencyAmount=100.0,
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
    Can only be used in `settings.ENVIRONMENT=local` environment.

    Test route for bulk inserting records.

    Returns a success message once the insertion is complete.
    """
    if not settings.ENVIRONMENT == "local":
        raise OnlyAvailableInLocalEnvError(
            function_name=bulk_insert_test.__name__,
        )

    try:
        # Perform the bulk insert
        bulk_insert_raw_sql(db, count)
        return {"message": "Successfully bulk inserted data."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk insert failed: {str(e)}")


@router.post(
    "/bulk-insert-users-and-verify",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=list[str],
)
async def bulk_insert_users_and_verify(count: int, db: Session = Depends(get_db)):
    """
    Can only be used in `settings.ENVIRONMENT=local` environment.

    Test route for bulk inserting users and verifying them.

    Returns the access tokens for the created users.
    """
    if not settings.ENVIRONMENT == "local":
        raise OnlyAvailableInLocalEnvError(
            function_name=bulk_insert_users_and_verify.__name__,
        )

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

    tokens = []
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8000"
        + settings.API_V1_STR,  # Only to be used in localhost testing
    ) as client:
        for user in users_create:
            login_data = {
                "username": user.username,
                "password": "testpassword",  # The password used during creation
            }
            response = await client.post("/login/access-token", data=login_data)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=500,
                    detail=f"User verification failed for {user.username}",
                )

            tokens.append(response.json()["access_token"])
            logger.debug(f"User {user.username} verified successfully.")

    return tokens
