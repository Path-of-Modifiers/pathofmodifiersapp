import pandas as pd


def summarize_function(*args) -> int:
    values = args[0]
    return values.get(0)


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
