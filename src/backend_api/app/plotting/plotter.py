import pandas as pd
from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Select

from app.core.models.models import Currency as model_Currency
from app.core.models.models import Item as model_Item
from app.core.models.models import ItemBaseType as model_ItemBaseType
from app.core.models.models import ItemModifier as model_ItemModifier
from app.core.schemas.plot import PlotData, PlotQuery
from app.exceptions.model_exceptions.plot_exception import (
    PlotNoModifiersProvidedError,
    PlotQueryDataNotFoundError,
)
from app.plotting.utils import find_conversion_value, summarize_function


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
            raise PlotNoModifiersProvidedError(
                query_data=query,
                function_name=self._init_query.__name__,
                class_name=self.__class__.__name__,
            )
        return statement

    def _item_spec_query(self, statement: Select, *, query: PlotQuery) -> Select:
        item_specifications = [
            model_Item.__dict__[key] == query.itemSpecifications.__dict__[key]
            for key in query.itemSpecifications.model_fields
            if (
                query.itemSpecifications.__dict__[key] is not None and "Ilvl" not in key
            )
        ]
        if query.itemSpecifications.minIlvl is not None:
            item_specifications.append(
                model_Item.ilvl >= query.itemSpecifications.minIlvl
            )

        if query.itemSpecifications.maxIlvl is not None:
            item_specifications.append(
                model_Item.ilvl <= query.itemSpecifications.maxIlvl
            )

        if item_specifications:
            return statement.where(*item_specifications)
        else:
            return statement

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
        # Sort values by date
        df.sort_values(by="createdAt", inplace=True)

        # Find most common currency
        most_common_currency_used = df.tradeName.mode()[0]

        # Find value in chaos
        value_in_chaos = df["currencyAmount"] * df["valueInChaos"]

        # Get timestamps of when the items were retrieved
        time_stamps = df["createdAt"]

        # Find conversion value between chaos and most common currency
        conversion_value = find_conversion_value(
            df,
            value_in_chaos=value_in_chaos,
            most_common_currency_used=most_common_currency_used,
        )
        value_in_most_common_currency_used = value_in_chaos / conversion_value

        return (
            value_in_chaos,
            time_stamps,
            value_in_most_common_currency_used,
            most_common_currency_used,
        )

    def _summarize_plot_data(
        self,
        value_in_chaos: pd.Series,
        time_stamps: pd.Series,
        value_in_most_common_currency_used: pd.Series,
        mostCommonCurrencyUsed: str,
    ) -> dict[str, pd.Series | str]:
        # Convert to dict
        plot_data = {
            "valueInChaos": value_in_chaos,
            "timeStamp": time_stamps,
            "valueInMostCommonCurrencyUsed": value_in_most_common_currency_used,
            "mostCommonCurrencyUsed": mostCommonCurrencyUsed,
        }
        # Then as a dataframe
        df = pd.DataFrame(plot_data)

        # Group by hour
        grouped_by_date_df = df.groupby(pd.Grouper(key="timeStamp", axis=0, freq="h"))

        # Aggregate by custom function
        agg_by_date_df = grouped_by_date_df.agg(
            {
                "valueInChaos": lambda values: summarize_function(values, 2),
                "valueInMostCommonCurrencyUsed": lambda values: summarize_function(
                    values, 2
                ),
            }
        )
        agg_by_date_df = agg_by_date_df.loc[~agg_by_date_df["valueInChaos"].isna()]

        # Update the values in the dict
        plot_data["timeStamp"] = agg_by_date_df.index
        plot_data["valueInChaos"] = agg_by_date_df["valueInChaos"].values
        plot_data["valueInMostCommonCurrencyUsed"] = agg_by_date_df[
            "valueInMostCommonCurrencyUsed"
        ].values

        return plot_data

    async def plot(self, db: AsyncSession, *, query: PlotQuery) -> PlotData:
        statement = self._init_query(query)
        statement = self._item_spec_query(statement, query=query)
        statement = self._base_spec_query(statement, query=query)
        statement = self._wanted_modifier_query(statement, query=query)

        result = await db.execute(statement)
        rows = result.mappings().all()
        df = pd.DataFrame(rows)

        if df.empty:
            raise PlotQueryDataNotFoundError(
                query_data=query,
                function_name=self.plot.__name__,
                class_name=self.__class__.__name__,
            )
        else:
            (
                value_in_chaos,
                time_stamps,
                value_in_most_common_currency_used,
                mostCommonCurrencyUsed,
            ) = self._create_plot_data(df)

        plot_data = self._summarize_plot_data(
            value_in_chaos,
            time_stamps,
            value_in_most_common_currency_used,
            mostCommonCurrencyUsed,
        )

        return self.validate(plot_data)
