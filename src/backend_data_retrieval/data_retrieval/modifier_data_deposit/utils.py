import logging
from io import StringIO
from typing import Any

import pandas as pd
import requests

from pom_api_authentication import get_superuser_token_headers

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="modifier_data_deposit.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)-8s:%(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def _chunks(lst, n):
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
) -> list[dict[str, Any]] | dict:
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
        return df_json
    elif request_method == "put":
        return df_json[0]
    else:
        raise NotImplementedError(
            f"df to json for the request method {request_method} is not implemented."
        )


def insert_data(
    df: pd.DataFrame,
    *,
    url: str,
    table_name: str,
    headers: dict[str, str] = None,
    logger: logging.Logger = None,
) -> None:
    if df.empty:
        return None
    data = df_to_JSON(df, request_method="post")
    response = requests.post(url + f"/{table_name}/", json=data, headers=headers)
    if response.status_code == 422:
        logger.warning(
            f"Recieved a 422 response, indicating an unprocessable entity was submitted, while posting a {table_name} table.\nSending smaller batches, trying to locate specific error."
        )
        for data_chunk in _chunks(data, n=15):
            response = requests.post(
                url + f"/{table_name}/", json=data_chunk, headers=headers
            )
            if response.status_code == 422:
                logger.warning(
                    "Located chunk of data that contains the unprocessable entity."
                )
                for individual_data in data_chunk:
                    response = requests.post(
                        url + f"/{table_name}/", json=individual_data, headers=headers
                    )
                    if response.status_code == 422:
                        logger.warning(
                            "Located the unprocessable entity:\n", individual_data
                        )
    elif response.status_code == 500:
        logger.critical("Recieved a 500 response, indicating client side error.")
        response.raise_for_status()

    elif response.status_code >= 300:
        response.raise_for_status()


def retrieve_data(*, url: str, table_name: str) -> pd.DataFrame | None:
    headers = get_superuser_token_headers(url)
    response = requests.get(url + f"/{table_name}/", headers=headers)

    df = pd.DataFrame()
    # Check if the request was successful
    if response.status_code == 200:
        # Load the JSON data into a pandas DataFrame
        json_io = StringIO(response.content.decode("utf-8"))
        df = pd.read_json(json_io, dtype=str)
        if df.empty:
            logger.info(
                f"Found no previously deposited data in the {table_name} table."
            )
            return None

        return df
    else:
        return None
