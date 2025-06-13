from typing import Literal

import numpy as np
import pandas as pd


def summarize_function(values: pd.Series, *args) -> float:
    return mean_of_bottom_p_wo_outliers(values, *args)


GROUP_INTERVAL_MULTIPLIER = 1.2


def mean_of_bottom_p_wo_outliers(values: pd.Series) -> float:
    n_values = len(values)

    min_value = min(values)
    filtered_values = values.loc[
        values.between(min_value, min_value * GROUP_INTERVAL_MULTIPLIER)
    ]

    while len(filtered_values) < min(5, np.ceil(n_values * 0.1)):
        values = values.loc[values.gt(min_value * GROUP_INTERVAL_MULTIPLIER)]
        n_values = len(values)

        min_value = min(values)
        filtered_values = values.loc[
            values.between(min_value, min_value * GROUP_INTERVAL_MULTIPLIER)
        ]

    mean_filtered_value = np.mean(filtered_values)
    return mean_filtered_value


def determine_confidence(values: pd.Series) -> Literal["low", "medium", "high"]:
    if len(values) < 20:
        return "low"
    elif len(values) < 30:
        return "medium"
    else:
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
