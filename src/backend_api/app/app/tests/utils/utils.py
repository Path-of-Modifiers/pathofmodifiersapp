from inspect import iscoroutinefunction
import os
import random
import string
from typing import Callable, List, Optional, Dict, Any, Union
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth
from sqlalchemy import inspect

from app.crud.base import ModelType


FIRST_SUPERUSER = os.getenv("FIRST_SUPERUSER")
FIRST_SUPERUSER_PASSWORD = os.getenv("FIRST_SUPERUSER_PASSWORD")


def random_lower_string(*, small_string: Optional[bool] = None) -> str:
    """Generate a random lowercase string.

    Args:
        small_string (Optional[bool], optional): Optional whether to have small string. Defaults to None.

    Returns:
        str: Random lowercase string.
    """
    random_lower_string = "".join(random.choices(string.ascii_lowercase, k=32))
    if small_string:
        random_lower_string = random_lower_string[:5]
    return random_lower_string


def random_int(
    *,
    small_int: Optional[bool] = None,
    big_int: Optional[bool] = None,
    negative: Optional[bool] = None,
    max_value: Optional[int] = None,
) -> int:
    """Generate a random integer.

    Args:
        small_int (Optional[bool], optional): Optional whether to have small integer. Defaults to None.
        big_int (Optional[bool], optional): Optional whether to have big integer. Defaults to None.
        negative (Optional[bool], optional): Optional whether to have negative integer. Defaults to None.
        max_value (Optional[int], optional): Optional to have max_value integer. Defaults to None.

    Returns:
        int: Random integer.
    """
    if max_value is not None:
        random_int = random.randint(1, max_value)
    elif small_int:
        random_int = random.randint(1, 32767)
    elif big_int:
        random_int = random.randint(1, 2**63 - 1)
    else:
        random_int = random.randint(1, 2**31 - 1)
    if negative:
        random_int = random_int * -1

    return random_int


def random_float(
    *,
    small_float: Optional[bool] = None,
    negative: Optional[bool] = None,
    max_value: Optional[int] = None,
) -> float:
    """Generate a random float.

    Args:
        small_float (Optional[bool], optional): Optional whether to have small float. Defaults to None.
        negative (Optional[bool], optional): Optional whether to have negative float. Defaults to None.
        max_value (Optional[int], optional): Optional to have max_value float. Defaults to None.

    Returns:
        float: Random float.
    """
    if max_value is not None:
        random_float = random.uniform(1, max_value)
    elif small_float:
        random_float = random.uniform(1, 32767)
    else:
        random_float = random.uniform(1, 10**10)
    if negative:
        random_float = random_float * -1
    return random_float


def random_bool() -> bool:
    """Generate a random boolean.

    Returns:
        bool: Random boolean.
    """
    return random.choice([True, False])


def random_json(key_type: Dict[str, bool]) -> Dict[str, Any]:
    """Generate a random JSON object based on the key_type dictionary.

    Args:
        key_type (Dict[str, bool]): Dictionary with the key and the type of the key.

    Returns:
        Dict[str, Any]: Random JSON object.
    """
    random_dict = {}
    for key in key_type:
        match key_type[key]:
            case "bool":
                random_dict[key] = random_bool()
            case "str":
                random_dict[key] = random_lower_string()
            case "int":
                random_dict[key] = random_int()
            case "float":
                random_dict[key] = random_float()
            case _:
                random_dict[key] = None

    return random_dict


def random_url() -> str:
    """Generate a random URL.

    Returns:
        str: Random URL.
    """
    return f"https://{random_lower_string()}.{random_lower_string(small_string=True)}"


def random_datetime() -> datetime:
    """Generate a random datetime.

    Returns:
        datetime: Random datetime.
    """
    return datetime.now() + random.uniform(-5, 5) * timedelta(days=1)


def random_based_on_type(reference: Union[str, float, int]) -> Union[str, int, float]:
    """Generate a random value based on the type of the reference.

    Args:
        reference (Union[str, float, int]): Reference object.

    Raises:
        NotImplementedError: If the type of the reference is not supported.

    Returns:
        Union[str, int, float]: Random value based on the type of the reference.
    """
    type_reference = type(reference)
    if type_reference == str:
        return random_lower_string()
    elif type_reference == float:
        return random_float(max_value=reference)
    elif type_reference == int:
        return random_int(max_value=reference)
    else:
        raise NotImplementedError(f"Objects of type {type_reference} is not supported")


def get_ignore_keys(model: ModelType, dict: Dict) -> List[str]:
    """Compare a model with a dictionary, and return the model's keys that are not in the dictionary

    Args:
        model (ModelType): Model
        dict (Dict): Dictionary
    """
    return [key for key in model.__table__.columns.keys() if key not in dict]


def is_courotine_function(func: Callable) -> bool:
    """Check if func is a coroutine function."""
    if iscoroutinefunction(func) and callable(func):
        return True
    else:
        return False


def get_model_unique_identifier(model: ModelType) -> str:
    """Get the unique identifier of a model.

    Important: Assumes the unique identifier is the first primary key of the model.

    Args:
        model (ModelType): Model

    Returns:
        str: Unique identifier of the model.
    """
    return inspect(model).primary_key[0].name


def get_model_table_name(model: ModelType) -> str:
    """Get the table name of a model.

    Args:
        model (ModelType): Model

    Returns:
        str: Table name of the model.
    """
    return model.__table__.name


def get_super_authentication() -> HTTPBasicAuth:
    """
    Get the super authentication for the Path of Modifiers API.

    Returns:
        HTTPBasicAuth: POM user and password authentication.
    """
    authentication = HTTPBasicAuth(FIRST_SUPERUSER, FIRST_SUPERUSER_PASSWORD)
    return authentication


def create_primary_key_map(obj: ModelType) -> Dict[str, Any]:
    """
    The CRUD get method uses filters. We can send in a map of primary keys to
    get the object we are looking for
    """
    object_map = {key.name: getattr(obj, key.name) for key in obj.__table__.primary_key}
    return object_map
