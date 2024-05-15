from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.sql.expression import Select
from pydantic import TypeAdapter
from fastapi import HTTPException
import pandas as pd

from .schemas import PlotQuery, PlotData
from app.core.models.models import Currency as model_Currency
from app.core.models.models import Item as model_Item
from app.core.models.models import ItemModifier as model_ItemModifier
from app.core.models.models import ItemBaseType as model_ItemBaseType


class Plotter:
    def __init__(self):
        self.validate = TypeAdapter(PlotData).validate_python

    def _init_query(self, query: PlotQuery) -> Select:
        league = query.league

        statement = (
            select(
                model_Item.itemId,
                model_Item.createdAt,
                model_Item.baseType,
                model_Item.currencyId,
                model_Item.currencyAmount,
                model_Currency.tradeName,
                model_Currency.valueInChaos,
                model_Currency.createdAt.label("currencyCreatedAt"),
            )
            .join_from(model_Currency, model_Item)
            .where(model_Item.league == league)
        )
        if len(query.wantedModifiers) == 0:
            raise HTTPException(
                status_code=406,
                detail="The plotting tool requires you to select at least one modifier",
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

    def _wanted_modifier_query(self, statement: Select, *, query: PlotQuery) -> Select:
        joined_statement = statement.join(model_ItemModifier)

        intersection_statement = None
        segments = []
        for wanted_modifier in query.wantedModifiers:
            modifier_id = wanted_modifier.modifierId
            modifier_limitation = wanted_modifier.modifierLimitations
            limitations = []
            if modifier_limitation is not None:
                # Adds limitations if they exist
                if wanted_modifier.modifierLimitations.minRoll is not None:
                    limitations.append(
                        model_ItemModifier.roll
                        >= wanted_modifier.modifierLimitations.minRoll
                    )
                if wanted_modifier.modifierLimitations.maxRoll is not None:
                    limitations.append(
                        model_ItemModifier.roll
                        <= wanted_modifier.modifierLimitations.maxRoll
                    )
                if wanted_modifier.modifierLimitations.textRoll is not None:
                    limitations.append(
                        model_ItemModifier.roll
                        == (wanted_modifier.modifierLimitations.textRoll)
                    )
            intersect_segment_statement = joined_statement.where(
                model_ItemModifier.modifierId == modifier_id, *limitations
            )
            segments.append(intersect_segment_statement)

        intersection_statement = joined_statement.intersect(*segments)
        return intersection_statement

    def _create_plot_data(self, df: pd.DataFrame) -> tuple:
        df.sort_values(by="createdAt", inplace=True)
        most_common_currency_used = df.tradeName.mode()[0]
        value_in_chaos = df["currencyAmount"] * df["valueInChaos"]
        conversionValue = value_in_chaos.copy(deep=True)
        time_stamps = df["createdAt"]

        most_common_currency_used_unique_ids = df.loc[
            df["tradeName"] == most_common_currency_used, "currencyId"
        ].unique()

        for id in most_common_currency_used_unique_ids:
            most_common_currency_value = df.loc[
                df["currencyId"] == id, "valueInChaos"
            ].iloc[0]
            most_common_currency_timestamp = df.loc[
                df["currencyId"] == id, "currencyCreatedAt"
            ].iloc[0]

            current_timestamp_mask = (
                df["currencyCreatedAt"] == most_common_currency_timestamp
            )
            conversionValue[current_timestamp_mask] = most_common_currency_value

        return value_in_chaos, time_stamps, most_common_currency_used, conversionValue

    async def plot(self, db: Session, *, query: PlotQuery) -> PlotData:
        statement = self._init_query(query)
        statement = self._item_spec_query(statement, query=query)
        statement = self._base_spec_query(statement, query=query)
        statement = self._wanted_modifier_query(statement, query=query)

        result = db.execute(statement).mappings().all()
        df = pd.DataFrame(result)
        if df.empty:
            raise HTTPException(
                status_code=404, detail="No data matching criteria found."
            )
        else:
            value_in_chaos, time_stamps, most_common_currency_used, conversionValue = (
                self._create_plot_data(df)
            )

        output_dict = {
            "valueInChaos": value_in_chaos,
            "timeStamp": time_stamps,
            "mostCommonCurrencyUsed": most_common_currency_used,
            "conversionValue": conversionValue,
        }

        return self.validate(output_dict)
