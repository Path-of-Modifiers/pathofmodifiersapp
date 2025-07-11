import logging
from collections.abc import Generator
from datetime import UTC, datetime
from typing import Any

import pandas as pd
import requests
from pydantic import HttpUrl

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.logs.logger import main_logger as logger


def _chunks(lst: list[Any], n: int) -> Generator[Any, None, None]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def remove_empty_fields(json_in: list[dict[str, str]]) -> list[dict[str, Any]]:
    json_out = []
    for obj in json_in:
        filtered_obj = {key: obj[key] for key in obj if obj[key] != ""}

        json_out.append(filtered_obj)

    return json_out


def df_to_JSON(
    df: pd.DataFrame | pd.Series, request_method: str
) -> list[dict[str, Any]] | dict[str, Any] | Any:
    logger.debug(f"Transforming data into JSON with request method {request_method}.")
    if isinstance(df, pd.Series):
        df = df.to_frame().transpose()
    with pd.option_context("future.no_silent_downcasting", True):
        df = df.replace(["nan", "None"], "").infer_objects(copy=False)
    df = df.fillna("")  # requests can not handle na
    df_json = df.to_dict(
        orient="records"
    )  # Converts to a list of dicts, where each dict is a row
    df_json = remove_empty_fields(df_json)  # Removes empty fields element-wise

    if request_method == "post":
        logger.debug("Transformed data into JSON for post method.")
        return df_json
    elif request_method == "put":
        logger.debug("Transformed data into JSON for put method.")
        return df_json[0]
    else:
        logger.exception("Invalid request method for df to json.")
        raise NotImplementedError(
            f"df to json for the request method {request_method} is not implemented."
        )


def find_hours_since_launch() -> int:
    current_time = datetime.now(UTC)
    league_launch_time = settings.LEAGUE_LAUNCH_DATETIME_OBJECT

    time_since_launch = current_time - league_launch_time

    days_since_launch, seconds_since_launch = (
        time_since_launch.days,
        time_since_launch.seconds,
    )
    hours_since_launch = days_since_launch * 24 + seconds_since_launch // 3600

    return hours_since_launch


def insert_data(
    df: pd.DataFrame,
    *,
    url: HttpUrl,
    table_name: str,
    logger: logging.Logger,
    on_duplicate_pkey_do_nothing: bool = False,
    headers: dict[str, str] | None = None,
) -> None:
    logger.debug("Inserting data into database.")
    if df.empty:
        logger.info(f"Found no data to insert into {table_name} table.")
        return None
    data = df_to_JSON(df, request_method="post")
    params = {"return_nothing": True}
    if on_duplicate_pkey_do_nothing:
        params["on_duplicate_pkey_do_nothing"] = True
    logger.debug("Sending data to database.")
    response = requests.post(
        f"{url}/{table_name}/", json=data, headers=headers, params=params
    )
    logger.debug("Sent request to insert data into the database.")
    if response.status_code == 422:
        logger.warning(
            f"Recieved a 422 response, indicating an unprocessable entity was submitted, while posting a {table_name} table.\nSending smaller batches, trying to locate specific error."
        )
        for data_chunk in _chunks(data, n=15):
            response = requests.post(
                f"{url}/{table_name}/", json=data_chunk, headers=headers
            )
            if response.status_code == 422:
                logger.warning(
                    "Located chunk of data that contains the unprocessable entity."
                )
                for individual_data in data_chunk:
                    response = requests.post(
                        f"{url}/{table_name}/", json=individual_data, headers=headers
                    )
                    if response.status_code == 422:
                        logger.warning(
                            "Located the unprocessable entity:\n", individual_data
                        )
    elif response.status_code == 500:
        logger.exception(
            f"Recieved a 500 response, indicating client side error. Error msg: {response.text[:10000]}"
        )
        response.raise_for_status()

    elif response.status_code >= 300:
        logger.exception(
            f"Recieved a {response.status_code} response. Error msg: {response.text[:10000]}"
        )
        response.raise_for_status()
