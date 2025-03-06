"""Added manual trigger for aggregation on unidentified item table

Revision ID: 2d92a782e970
Revises: 62c3fbcdc773
Create Date: 2025-03-04 11:48:24.463854

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.alembic.replaceable_objects.main import ReplaceableObject, ReplaceableTrigger


# revision identifiers, used by Alembic.
revision: str = "2d92a782e970"
down_revision: Union[str, None] = "62c3fbcdc773"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Seems like alembic messes up capitalization

unidentified_item_view = ReplaceableObject(
    "unidentifiedItemView",
    """
    SELECT name, unid."itemBaseTypeId", unid."createdHoursSinceLaunch", league, unid."currencyId", ilvl, unid."currencyAmount", unid."nItems", identified, rarity
        FROM unidentified_item as unid
    """,
)

unidentified_aggregation_trigger = ReplaceableTrigger(
    "aggregate_unidentified",
    """
    RETURNS trigger AS $aggregate_unidentified$
    DECLARE
    	n_items INT;
    	current_average FLOAT;
    	id INT;
    BEGIN
    	IF EXISTS (SELECT 1
    			FROM unidentified_item AS unid
    			WHERE name=NEW.name AND unid."createdHoursSinceLaunch"=NEW."createdHoursSinceLaunch"
    			AND ilvl=NEW.ilvl AND league=NEW.league)
    		THEN
    			SELECT unid."nItems", unid."currencyAmount", unid."unidentifiedItemId"  INTO n_items, current_average, id
    			FROM unidentified_item AS unid
    			WHERE name=NEW.name AND unid."createdHoursSinceLaunch"=NEW."createdHoursSinceLaunch"
    			AND ilvl=NEW.ilvl AND league=NEW.league;
    			UPDATE unidentified_item
    				SET unid."currencyAmount" = n_items + 1,
    				unid."currencyAmount" = ((current_average * n_items) + NEW."currencyAmount")/(n_items + 1)
    				WHERE unid."unidentifiedItemId"=id;
    		ELSE
    			--INSERT INTO unidentified_item AS unid (name, unid."itemBaseTypeId", unid."createdHoursSinceLaunch", league, unid."currencyId", ilvl, unid."currencyAmount", unid."nItems", identified, rarity)
    			INSERT INTO unidentified_item (name, itemBaseTypeId, createdHoursSinceLaunch, league, currencyId, ilvl, currencyAmount, nItems, identified, rarity)
    			VALUES (
    				NEW.name,
                    NEW."itemBaseTypeId",
    				NEW."createdHoursSinceLaunch",
    				NEW.league,
    				NEW."currencyId",
    				NEW.ilvl,
    				NEW."currencyAmount",
    				1,
                    NEW.identified,
                    NEW.rarity
    				);
    		END IF;
    	RETURN NEW;
    END;
    $aggregate_unidentified$ LANGUAGE plpgsql;
    """,
    # 'RETURNS trigger AS $aggregate_unidentified$ DECLARE n_items INT; current_average FLOAT; id INT; BEGIN IF EXISTS (SELECT 1 FROM unidentified_item WHERE name=NEW.name AND unid."createdHoursSinceLaunch"=NEW."createdHoursSinceLaunch" AND ilvl=NEW.ilvl AND league=NEW.league) THEN SELECT unid."nItems", unid."currencyAmount", unid."unidentifiedItemId"  INTO n_items, current_average, id FROM unidentified_item WHERE name=NEW.name AND unid."createdHoursSinceLaunch"=NEW."createdHoursSinceLaunch" AND ilvl=NEW.ilvl AND league=NEW.league; UPDATE unidentified_item SET unid."currencyAmount" = n_items + 1, unid."currencyAmount" = ((current_average * n_items) + NEW."currencyAmount")/(n_items + 1) WHERE unid."unidentifiedItemId"=id;ELSE INSERT INTO unidentified_item (name, unid."itemBaseTypeId", unid."createdHoursSinceLaunch", league, unid."currencyId", ilvl, unid."currencyAmount", unid."nItems", identified, rarity) VALUES (NEW.name,NEW."itemBaseTypeId",NEW."createdHoursSinceLaunch",NEW.league,NEW."currencyId",NEW.ilvl,NEW."currencyAmount",1,NEW.identified,NEW.rarity);END IF;RETURN NEW;END;$aggregate_unidentified$ LANGUAGE plpgsql;',
    """
    INSTEAD OF INSERT ON unidentifiedItemView 
	FOR EACH ROW EXECUTE FUNCTION aggregate_unidentified()
    """,
)


def upgrade() -> None:
    op.create_view(unidentified_item_view)
    op.create_trigger(unidentified_aggregation_trigger)


def downgrade() -> None:
    op.drop_view(unidentified_item_view)
    op.drop_trigger(unidentified_aggregation_trigger)
