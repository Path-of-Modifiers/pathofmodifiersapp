from sqlalchemy.orm import Session, Bundle
from sqlalchemy import select, union_all
from sqlalchemy.sql.expression import Select
from sqlalchemy.engine import CursorResult

from .schemas import PlotQuery, PlotData
from app.core.models.models import Currency as model_Currency
from app.core.models.models import Item as model_Item
from app.core.models.models import ItemModifier as model_ItemModifier
from app.core.models.models import ItemBaseType as model_ItemBaseType
from app.core.models.models import Stash as model_Stash


class Plotter:
    def __init__(self):
        pass

    def _init_query(self, query: PlotQuery) -> Select:
        league = query.league

        statement = (
            select(
                Bundle(
                    "item",
                    model_Item.itemId,
                    model_Item.baseType,
                    model_Item.currencyId,
                    model_Item.currencyAmount,
                ),
                Bundle("currency", model_Currency.tradeName),
                Bundle("stash", model_Stash.accountName),
            )
            .join_from(model_Currency, model_Item)
            .join_from(model_Currency, model_Stash)
            .where(model_Item.league == league)
        )
        return statement

    def _item_spec_query(self, statement: Select, *, query: PlotQuery) -> Select:
        item_specifications = [
            model_Item.__dict__[key] == query.itemSpecifications.__dict__[key]
            for key in query.itemSpecifications.model_fields
            if query.itemSpecifications.__dict__[key] is not None
        ]

        return statement.where(*item_specifications)

    def _base_spec_query(self, statement: Select, *, query: PlotQuery) -> Select:
        if query.baseSpecifications is not None:
            base_specifications = [
                model_ItemBaseType.__dict__[key]
                == query.baseSpecifications.__dict__[key]
                for key in query.baseSpecifications.model_fields
                if query.baseSpecifications.__dict__[key] is not None
            ]
            statement = statement.join(model_ItemBaseType).where(*base_specifications)

        return statement

    def _modifier_id_query(self, statement: Select, *, query: PlotQuery) -> Select:
        modifier_ids = [
            wanted_modifier.modifierId for wanted_modifier in query.wantedModifiers
        ]

        statement = statement.join(model_ItemModifier).where(
            model_ItemModifier.modifierId.in_(modifier_ids)
        )

        return statement

    def _modifier_limitation_query(
        self, statement: Select, *, query: PlotQuery
    ) -> Select:
        modifier_limitations = [
            wanted_modifier.modifierLimitations
            for wanted_modifier in query.wantedModifiers
            if wanted_modifier.modifierLimitations is not None
        ]

        if modifier_limitations:  # Checks if there was any limitations
            statement_w_limitations = []
            for (
                wanted_modifier
            ) in query.wantedModifiers:  # Goes through the limitations of each modifier
                if (
                    wanted_modifier.modifierLimitations is not None
                ):  # check if modifier has a limitation
                    limitations = []
                    # Adds limitations if they exist
                    if wanted_modifier.modifierLimitations.minRoll is not None:
                        limitations.append(
                            model_ItemModifier.roll
                            >= wanted_modifier.modifierLimitations.minRoll
                        )
                    elif wanted_modifier.modifierLimitations.maxRoll is not None:
                        limitations.append(
                            model_ItemModifier.roll
                            <= wanted_modifier.modifierLimitations.maxRoll
                        )
                    elif wanted_modifier.modifierLimitations.textRoll is not None:
                        limitations.append(
                            model_ItemModifier.roll
                            == wanted_modifier.modifierLimitations.textRoll
                        )
                    # Adding the limitations to the statement
                    limitation_statement = statement.where(*limitations)
                    statement_w_limitations.append(limitation_statement)
                else:
                    pass
            union_statement = union_all(*statement_w_limitations)
            statement = statement.from_statement(union_statement)

        return statement

    def _create_plot_data(self, result: CursorResult) -> PlotData:
        pass

    def plot(self, db: Session, *, query: PlotQuery) -> PlotData:
        statement = self._init_query(query)
        statement = self._item_spec_query(statement, query=query)
        statement = self._base_spec_query(statement, query=query)
        statement = self._modifier_id_query(statement, query=query)
        statement = self._modifier_limitation_query(statement, query=query)

        result = db.execute(statement)
        for row in result:
            # print(
            #     f"createdAt: {row.item.createdAt}, price: {row.item.currencyAmount}, currencyId: {row.currency.tradeName}"
            # )
            print(row)
