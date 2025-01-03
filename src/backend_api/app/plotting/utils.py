from typing import Literal

import pandas as pd


def summarize_function(values: pd.Series) -> int:
    return values.iat[0]


def determine_confidence(
    values: pd.Series,  # noqa: ARG001
) -> Literal["low", "medium", "high"]:
    return "high"


def find_conversion_value(
    df: pd.DataFrame,
    *,
    value_in_chaos: pd.Series,
    most_common_currency_used: str,
) -> pd.Series:
    most_common_currency_used_unique_ids = df.loc[
        df["tradeName"] == most_common_currency_used, "currencyId"
    ].unique()
    conversion_value = value_in_chaos.copy(deep=True)

    for id in most_common_currency_used_unique_ids:
        most_common_currency_value = df.loc[
            df["currencyId"] == id, "valueInChaos"
        ].iloc[0]
        most_common_currency_timestamp = df.loc[
            df["currencyId"] == id, "currencyCreatedHoursSinceLaunch"
        ].iloc[0]

        current_timestamp_mask = (
            df["currencyCreatedHoursSinceLaunch"] == most_common_currency_timestamp
        )
        conversion_value[current_timestamp_mask] = most_common_currency_value

    return conversion_value
