import numpy as np
import pandas as pd


def summarize_function(values: pd.Series, *args) -> int:
    return mean_of_top_n_values(values, *args)


def mean_of_top_n_values(values: pd.Series, N: int) -> int:
    n_values = len(values)
    if n_values > 100:
        n_values = 100
    chosen_values = values.iloc[:n_values]

    mean_value = np.mean(chosen_values)
    std_value = np.std(chosen_values)

    filtered_values = chosen_values.loc[abs(chosen_values - mean_value) < N * std_value]

    mean_filtered_value = np.mean(filtered_values)
    return mean_filtered_value


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
            df["currencyId"] == id, "currencyCreatedAt"
        ].iloc[0]

        current_timestamp_mask = (
            df["currencyCreatedAt"] == most_common_currency_timestamp
        )
        conversion_value[current_timestamp_mask] = most_common_currency_value

    return conversion_value
