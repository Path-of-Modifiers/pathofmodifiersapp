"""Added unidentified aggregation job

Revision ID: e38727349f3f
Revises: 0f3f15f56b7d
Create Date: 2025-03-31 14:15:02.926141

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.alembic.replaceable_objects.main import ReplaceableTrigger


# revision identifiers, used by Alembic.
revision: str = "e38727349f3f"
down_revision: Union[str, None] = "0f3f15f56b7d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


unidentified_aggregation_trigger = ReplaceableTrigger(
    "aggregate_unidentified",
    "unidentified_item",
    """
    RETURNS TRIGGER AS $aggregate_unidentified$
        DECLARE
            current_hour INT;
            divine_id INT;
            divine_value FLOAT;
        BEGIN
			IF EXISTS (SELECT 1 FROM unidentified_item AS unid WHERE unid."createdHoursSinceLaunch" = NEW."createdHoursSinceLaunch") THEN
				RETURN NEW;
			END IF;
			
            current_hour := (SELECT MAX(unid."createdHoursSinceLaunch") FROM unidentified_item AS unid);
            divine_id := (SELECT MAX(cur."currencyId") FROM currency AS cur WHERE cur."tradeName"='divine');
            divine_value := (SELECT cur."valueInChaos" FROM currency AS cur WHERE cur."currencyId"=divine_id);
			

            WITH aggregates AS (
                SELECT name, unid."itemBaseTypeId", unid."createdHoursSinceLaunch", league, ilvl, stddev(unid."currencyAmount" * cur."valueInChaos") AS std, AVG(unid."currencyAmount" * cur."valueInChaos") AS calc_avg, COUNT(unid."itemId") AS calc_count
                FROM unidentified_item AS unid
                NATURAL JOIN currency as cur
                WHERE unid."createdHoursSinceLaunch" = current_hour
				AND NOT aggregated
                GROUP BY name, unid."itemBaseTypeId", unid."createdHoursSinceLaunch", league, ilvl
            ), affected_item_ids AS (
                SELECT unid."itemId" FROM unidentified_item AS unid WHERE NOT aggregated AND unid."createdHoursSinceLaunch"=current_hour
            )

            INSERT INTO unidentified_item (name, "itemBaseTypeId", "createdHoursSinceLaunch", league, "currencyId", ilvl, "currencyAmount", "nItems", identified, rarity, aggregated)
                SELECT name, unid."itemBaseTypeId", unid."createdHoursSinceLaunch", league, divine_id, ilvl, AVG(unid."currencyAmount" * cur."valueInChaos") / divine_value, calc_count, identified, rarity, TRUE
                    FROM unidentified_item AS unid
                    NATURAL JOIN aggregates
                    NATURAL JOIN currency AS cur
                    WHERE unid."currencyAmount" * cur."valueInChaos" <= calc_avg + 1.97 * std
                    	AND unid."currencyAmount" * cur."valueInChaos" >= calc_avg - 1.97 * std
                    GROUP BY name, unid."itemBaseTypeId", unid."createdHoursSinceLaunch", league, ilvl, identified, rarity, calc_count;
			
			DELETE FROM unidentified_item as unid
				WHERE NOT aggregated AND unid."createdHoursSinceLaunch"=current_hour;
			
			RETURN NEW;
		END;
    $aggregate_unidentified$ LANGUAGE plpgsql;
    """,
    """
    BEFORE INSERT ON unidentified_item
	FOR EACH ROW
	EXECUTE FUNCTION aggregate_unidentified();
    """,
)


def upgrade() -> None:
    op.create_trigger(unidentified_aggregation_trigger)


def downgrade() -> None:
    op.drop_trigger(unidentified_aggregation_trigger)
