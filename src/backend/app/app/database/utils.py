import requests
import pandas as pd
from typing import List, Dict, Any, Union


def remove_empty_fields(json_in: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    json_out = []
    for obj in json_in:
        filtered_obj = {key: obj[key] for key in obj if obj[key]}

        json_out.append(filtered_obj)

    return json_out


def df_to_JSON(
    df: Union[pd.DataFrame, pd.Series], request_method: str
) -> Union[List[Dict[str, Any]], Dict]:
    if isinstance(df, pd.Series):
        df = df.to_frame().transpose()
    df = df.replace(["nan", "None"], pd.NA)
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


def insert_data(df: pd.DataFrame, *, url: str, table_name: str) -> None:
    if df.empty:
        return None
    data = df_to_JSON(df, request_method="post")
    response = requests.post(url + f"/{table_name}/", json=data)
    if response.status_code >= 300:
        if response.status_code == 422:
            for data_json in data:
                response = requests.post(url + f"/{table_name}/", json=data_json)
                if response.status_code >= 300:
                    print(data_json)
                    response.raise_for_status()
        print(data)

        response.raise_for_status()


def retrieve_data(*, url: str, table_name: str) -> pd.DataFrame | None:
    df = pd.read_json(url + f"/{table_name}/", dtype=str)
    if df.empty:
        return None
    return df
