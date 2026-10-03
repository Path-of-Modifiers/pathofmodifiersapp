from collections import defaultdict
from collections.abc import Iterable
from typing import Any

from backend_api.app.core.models.models import Item as model_Item
from backend_api.app.core.models.models import (
    ItemAvailability as model_ItemAvailability,
)
from backend_api.app.core.models.models import ItemModifier as model_ItemModifier
from backend_api.app.core.schemas.item import (
    Item,
    ItemAvailability,
    ItemAvailabilityExpired,
    ItemAvailabilityUpdated,
    ItemBase,
    ItemCreate,
)
from backend_api.app.crud.base import CRUDBase
from pydantic import TypeAdapter
from sqlalchemy import (
    Boolean,
    Float,
    Integer,
    String,
    column,
    delete,
    select,
    update,
    values,
)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session


class CRUDItem:
    def __init__(self):
        self.crud_base = CRUDBase[model_Item, Item, Any, Any](
            model=model_Item, schema=Item, create_schema=None
        )

        self.item_base_adapter = TypeAdapter(list[ItemBase])

        self.item_validate = TypeAdapter(list[Item]).validate_python

        self.item_availability_validate = TypeAdapter(
            list[ItemAvailability]
        ).validate_python

    async def get(self, *args, **kwargs):
        return await self.crud_base.get(*args, **kwargs)

    async def _incoming_to_database_map(
        self, db: Session, *, incoming: Iterable[tuple[str, int]]
    ) -> dict[tuple[str, int], int]:
        incoming_items_table = values(
            column("game_item_id", String),
            column("league_id", Integer),
            name="incoming_items",
        ).data(incoming)

        incoming_to_database_ids_stmt = select(
            model_Item.itemId,
            model_Item.gameItemId,
            model_Item.leagueId,
        ).join(
            incoming_items_table,
            (model_Item.leagueId == incoming_items_table.c.league_id)
            & (model_Item.gameItemId == incoming_items_table.c.game_item_id),
        )

        incoming_items = db.execute(incoming_to_database_ids_stmt).mappings().all()

        return {
            (incoming.gameItemId, incoming.leagueId): incoming.itemId
            for incoming in incoming_items
        }

    async def create_items(
        self, db: Session, *, new_items: list[ItemCreate]
    ) -> list[Item]:
        if not new_items:
            return []

        # Deduplicates update_availability, only caring about the latest price
        latest_by_item = {
            (item.item.gameItemId, item.item.leagueId): item for item in new_items
        }
        new_items = list(latest_by_item.values())

        incoming_to_database = await self._incoming_to_database_map(
            db, incoming=latest_by_item.keys()
        )

        truely_new_items = list[ItemCreate]()
        existing_items = list[ItemCreate]()

        for item in new_items:
            game_item_id = item.item.gameItemId
            league_id = item.item.leagueId

            db_item_id = incoming_to_database.get((game_item_id, league_id))
            if db_item_id is None:
                truely_new_items.append(item)
            else:
                existing_items.append(item)

        db_items = list[model_Item]()
        for new_item in truely_new_items:
            db_items.append(model_Item(**new_item.item.model_dump()))

        db.add_all(db_items)
        db.flush()

        db_item_availability = list[model_ItemAvailability]()

        instance_count = defaultdict[tuple[int, int], int](int)
        db_item_modifiers = list[model_ItemModifier]()
        for db_item, new_item in zip(db_items, truely_new_items, strict=True):
            for modifier in new_item.modifiers:
                key = (db_item.itemId, modifier.modifierId)
                for roll in modifier.rolls:
                    db_item_modifiers.append(
                        model_ItemModifier(
                            itemId=db_item.itemId,
                            modifierId=modifier.modifierId,
                            position=roll.position,
                            instance=instance_count[key],
                            roll=roll.roll,
                        )
                    )
                # a modifier can appear multiple times on an item (eg. forbidden shako)
                instance_count[key] += 1

            db_item_availability.append(
                model_ItemAvailability(
                    itemId=db_item.itemId,
                    currencyId=new_item.price.currencyId,
                    currencyAmount=new_item.price.currencyAmount,
                    validFrom=new_item.item.firstObserved,
                    isAsync=new_item.price.isAsync,
                )
            )

        db.add_all(db_item_modifiers)

        for existing_item in existing_items:
            game_item_id = existing_item.item.gameItemId
            league_id = existing_item.item.leagueId

            db_item_id = incoming_to_database[(game_item_id, league_id)]

            db_item_availability.append(
                model_ItemAvailability(
                    itemId=db_item_id,
                    currencyId=existing_item.price.currencyId,
                    currencyAmount=existing_item.price.currencyAmount,
                    validFrom=existing_item.item.firstObserved,
                    isAsync=existing_item.price.isAsync,
                )
            )

        db.add_all(db_item_availability)
        db.flush()
        db.commit()

        return self.item_validate(db_items)

    async def update_availability(
        self, db: Session, *, updated_availability: list[ItemAvailabilityUpdated]
    ) -> list[ItemAvailability]:
        if not updated_availability:
            return []
        # Deduplicates update_availability, only caring about the latest price
        latest_by_item = {
            (item.gameItemId, item.leagueId): item for item in updated_availability
        }
        updated_availability = list(latest_by_item.values())

        incoming_to_database = await self._incoming_to_database_map(
            db, incoming=latest_by_item.keys()
        )

        # removes items not already in the db
        incoming_data = list[tuple[int, int, float, int, bool]]()
        for item in updated_availability:
            item_id = incoming_to_database.get((item.gameItemId, item.leagueId))
            if item_id is None:
                continue

            incoming_data.append(
                (
                    item_id,
                    item.price.currencyId,
                    item.price.currencyAmount,
                    item.validFrom,
                    item.price.isAsync,
                )
            )

        if not incoming_data:
            return []

        incoming_table = values(
            column("item_id", Integer),
            column("currency_id", Integer),
            column("currency_amount", Float),
            column("valid_from", Integer),
            column("is_async", Boolean),
            name="incoming",
        ).data(incoming_data)
        # 1. Delete existing same-hour availability
        db.execute(
            delete(model_ItemAvailability).where(
                model_ItemAvailability.itemId == incoming_table.c.item_id,
                model_ItemAvailability.validFrom == incoming_table.c.valid_from,
            )
        )

        # 2. Close current availability
        db.execute(
            update(model_ItemAvailability)
            .where(
                model_ItemAvailability.itemId == incoming_table.c.item_id,
                model_ItemAvailability.validTo.is_(None),
            )
            .values(
                validTo=incoming_table.c.valid_from,
            )
        )

        # 3. Insert the new availability
        new_availability = (
            db.execute(
                insert(model_ItemAvailability).from_select(
                    [
                        "itemId",
                        "currencyId",
                        "currencyAmount",
                        "validFrom",
                        "isAsync",
                    ],
                    select(
                        incoming_table.c.item_id,
                        incoming_table.c.currency_id,
                        incoming_table.c.currency_amount,
                        incoming_table.c.valid_from,
                        incoming_table.c.is_async,
                    ),
                )
            )
            .scalars()
            .all()
        )

        db.commit()
        return self.item_availability_validate(new_availability)

    async def patch_expired_availability(
        self, db: Session, *, expired_availability: list[ItemAvailabilityExpired]
    ) -> list[ItemAvailability]:
        if not expired_availability:
            return []
        incoming_to_database = await self._incoming_to_database_map(
            db,
            incoming=[
                (item.gameItemId, item.leagueId) for item in expired_availability
            ],
        )

        # removes items which don't already exist in db
        expired_data = list[tuple[str, int]]()
        for item in expired_availability:
            item_id = incoming_to_database.get((item.gameItemId, item.leagueId))
            if item_id is None:
                continue

            expired_data.append((item_id, item.validTo))

        if not expired_data:
            return []

        expired_table = values(
            column("item_id", Integer),
            column("valid_to", Integer),
            name="expired",
        ).data(expired_data)
        # 1. Delete existing same-hour availability
        db.execute(
            delete(model_ItemAvailability).where(
                model_ItemAvailability.itemId == expired_table.c.item_id,
                model_ItemAvailability.validFrom == expired_table.c.valid_to,
            )
        )

        # 2. Close current availability
        updated_availability = (
            db.execute(
                update(model_ItemAvailability)
                .where(
                    model_ItemAvailability.itemId == expired_table.c.item_id,
                    model_ItemAvailability.validTo.is_(None),
                )
                .values(
                    validTo=expired_table.c.valid_to,
                )
            )
            .scalars()
            .all()
        )

        db.commit()

        return self.item_availability_validate(updated_availability)
