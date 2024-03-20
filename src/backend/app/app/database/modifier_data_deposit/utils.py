from typing import List, Dict, Any


def remove_empty_fields(json_in: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    json_out = []
    for obj in json_in:
        filtered_obj = {key: obj[key] for key in obj if obj[key]}

        json_out.append(filtered_obj)

    return json_out
