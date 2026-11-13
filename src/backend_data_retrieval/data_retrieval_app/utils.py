import logging
from collections import defaultdict
from collections.abc import Generator
from datetime import UTC, datetime
from typing import Any, Literal

import pandas as pd
import requests
from backend_api.app.core.schemas.item_base_type import ItemBaseType
from backend_api.app.core.schemas.league import League
from backend_api.app.core.schemas.modifier import (
    GroupedModifier,
    GroupedModifierWUniques,
)
from backend_api.app.core.schemas.table_version import TableVersion
from backend_api.app.core.schemas.unique_item import UniqueItem
from pydantic import HttpUrl, TypeAdapter

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.logs.logger import db_retrieval_logger, main_logger


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
    main_logger.debug(
        f"Transforming data into JSON with request method {request_method}."
    )
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
        main_logger.debug("Transformed data into JSON for post method.")
        return df_json
    elif request_method == "put":
        main_logger.debug("Transformed data into JSON for put method.")
        return df_json[0]
    else:
        main_logger.exception("Invalid request method for df to json.")
        raise NotImplementedError(
            f"df to json for the request method {request_method} is not implemented."
        )


def find_hours_since_launch(leagues: list[League]) -> dict[int, int]:
    """
    Finds the number of hours since launch for each of the leagues in the given dataframe
    """
    current_time = datetime.now(UTC)
    hours_since_launch_dict = dict[int, int]()
    for league in leagues:
        time_since_launch = current_time - league.validFrom

        days_since_launch, seconds_since_launch = (
            time_since_launch.days,
            time_since_launch.seconds,
        )
        hours_since_launch = days_since_launch * 24 + seconds_since_launch // 3600
        hours_since_launch_dict[league.leagueId] = hours_since_launch

    return hours_since_launch_dict


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


def get_data_safe(
    url: str,
    *,
    logger: logging.Logger = None,
    params: dict | list = None,
    headers: dict[str, str] | None = None,
) -> requests.Response:
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
    except Exception as e:
        if logger is not None:
            logger.error(
                f"The following error occurred while making request a get request to {url}: {e}"
            )
        raise e

    return response


def send_request_safe(
    method: Literal["get", "put", "patch", "post", "delete"],
    url: str,
    *args,
    logger: logging.Logger = None,
    **kwargs,
) -> requests.Response:
    method_func = None
    if method == "get":
        method_func = requests.get
    elif method == "put":
        method_func = requests.put
    elif method == "patch":
        method_func = requests.patch
    elif method == "post":
        method_func = requests.post
    elif method == "delete":
        method_func = requests.delete
    else:
        raise ValueError(
            f"Invalid method ({method}), must be one of: get, put, patch, post, delete"
        )
    try:
        response = method_func(url, *args, **kwargs)
        response.raise_for_status()
    except Exception as e:
        if logger is not None:
            logger.error(
                f"The following error occurred while making request a {method} request to {url}: {e}"
            )
        raise e

    return response


def get_leagues(headers: dict) -> list[League]:
    response = send_request_safe(
        "get",
        f"{settings.BACKEND_BASE_URL}/league/",
        headers=headers,
        logger=db_retrieval_logger,
    )

    return TypeAdapter(list[League]).validate_python(response.json())


def get_leagues_active(headers: dict) -> list[League]:
    response = send_request_safe(
        "get",
        f"{settings.BACKEND_BASE_URL}/league/active/",
        headers=headers,
        logger=db_retrieval_logger,
    )

    return TypeAdapter(list[League]).validate_python(response.json())


def get_grouped_modifiers(headers: dict) -> list[GroupedModifier]:
    response = send_request_safe(
        "get",
        f"{settings.BACKEND_BASE_URL}/modifier/grouped/",
        headers=headers,
        logger=db_retrieval_logger,
    )
    modifiers = TypeAdapter(list[GroupedModifier]).validate_python(response.json())
    return modifiers


def get_grouped_modifiers_w_uniques(headers: dict) -> list[GroupedModifierWUniques]:
    response = send_request_safe(
        "get",
        f"{settings.BACKEND_BASE_URL}/modifier/grouped/uniqueItem/",
        headers=headers,
        logger=db_retrieval_logger,
    )
    modifiers = TypeAdapter(list[GroupedModifierWUniques]).validate_python(
        response.json()
    )
    return modifiers


def get_grouped_modifiers_by_unique(
    headers: dict,
) -> dict[str, list[GroupedModifierWUniques]]:
    modifiers = get_grouped_modifiers_w_uniques(headers)

    modifiers_by_unique = defaultdict[str, list[GroupedModifierWUniques]](list)
    for modifier in modifiers:
        uniques = modifier.uniques
        for unique in uniques:
            modifiers_by_unique[unique.name].append(modifier)

    return dict(modifiers_by_unique)


def get_item_base_types(headers: dict) -> list[ItemBaseType]:
    response = send_request_safe(
        "get",
        f"{settings.BACKEND_BASE_URL}/itemBaseType/",
        headers=headers,
        logger=db_retrieval_logger,
    )
    base_types = TypeAdapter(list[ItemBaseType]).validate_python(response.json())
    return base_types


def get_item_base_type_id_by_name(headers: dict) -> dict[str, int]:
    base_types = get_item_base_types(headers)
    base_type_ids = {
        base_type.baseType: base_type.itemBaseTypeId for base_type in base_types
    }
    return base_type_ids


def get_uniques(headers: dict) -> list[UniqueItem]:
    response = send_request_safe(
        "get",
        f"{settings.BACKEND_BASE_URL}/uniqueItem/",
        headers=headers,
        logger=db_retrieval_logger,
    )
    return TypeAdapter(list[UniqueItem]).validate_python(response.json())


def get_uniques_by_name_and_basetype_id(
    headers: dict,
) -> dict[tuple[str, int], UniqueItem]:
    uniques = get_uniques(headers)

    return {(unique.name, unique.itemBaseTypeId): unique for unique in uniques}


def get_table_version(table: str, headers: dict) -> TableVersion | None:
    response = send_request_safe(
        "get",
        f"{settings.BACKEND_BASE_URL}/tableVersion/{table}",
        headers=headers,
        logger=db_retrieval_logger,
    )
    return TypeAdapter(TableVersion | None).validate_python(response.json())
