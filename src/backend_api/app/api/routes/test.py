from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.api.deps import (
    get_current_active_superuser,
    get_db,
)
from app.core.models.models import Item
from app.core.schemas.item import ItemCreate

router = APIRouter()


test_prefix = "test"


def bulk_insert_raw_sql(db: Session):
    # Generate dummy data for 100,000 objects
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
        for i in range(100000)
    ]

    # Prepare the raw SQL statement for bulk insert
    create_stmt = insert(Item)
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
    db: Session = Depends(get_db),
):
    """
    Test route for bulk inserting 100,000 account records.

    Returns a success message once the insertion is complete.
    """
    try:
        # Perform the bulk insert
        bulk_insert_raw_sql(db)
        return {"message": "Successfully inserted 100,000 data."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk insert failed: {str(e)}")
