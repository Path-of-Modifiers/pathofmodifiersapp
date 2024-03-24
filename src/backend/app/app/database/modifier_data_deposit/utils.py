from typing import List, Dict, Any, Union
import pandas as pd


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
