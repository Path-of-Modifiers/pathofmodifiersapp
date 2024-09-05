import random
import string
from collections.abc import Callable
from datetime import datetime, timedelta
from inspect import iscoroutinefunction
from typing import Any

from fastapi.testclient import TestClient
from sqlalchemy import inspect

from app.core.config import settings
from app.crud.base import ModelType


def random_lower_string(*, small_string: bool | None = None) -> str:
    """Generate a random lowercase string.

    Args:
        small_string (bool | None): Optional whether to have small string. Defaults to None.

    Returns:
        str: Random lowercase string.
    """
    random_lower_string = "".join(random.choices(string.ascii_lowercase, k=32))
    if small_string:
        random_lower_string = random_lower_string[:5]
    return random_lower_string


def random_int(
    *,
    small_int: bool | None = None,
    big_int: bool | None = None,
    negative: bool | None = None,
    max_value: int | None = None,
) -> int:
    """Generate a random integer.

    Args:
        small_int (bool | None): Optional whether to have small integer. Defaults to None.
        big_int (bool | None): Optional whether to have big integer. Defaults to None.
        negative (bool | None): Optional whether to have negative integer. Defaults to None.
        max_value (int | None): Optional to have max_value integer. Defaults to None.

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
    small_float: bool | None = None,
    negative: bool | None = None,
    max_value: int | None = None,
) -> float:
    """Generate a random float.

    Args:
        small_float (bool | None): Optional whether to have small float. Defaults to None.
        negative (bool | None): Optional whether to have negative float. Defaults to None.
        max_value (int] | None): Optional to have max_value float. Defaults to None.

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


def random_json(key_type: dict[str, bool]) -> dict[str, Any]:
    """Generate a random JSON object based on the key_type dictionary.

    Args:
        key_type (Dict[str, bool): Dictionary with the key and the type of the key.

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


def random_based_on_type(reference: str | float | int) -> str | int | float:
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


def random_email() -> str:
    """Generate a random email.

    Returns:
        str: Random email.
    """
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_ignore_keys(model: ModelType, dict: dict) -> list[str]:
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
    return model.__tablename__


def get_superuser_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


def create_random_ip() -> str:
    """
    Create a random IP address.

    Returns:
        str: Random IP address.
    """
    return ".".join(str(random.randint(0, 255)) for _ in range(4))


def get_extract_functions(compare_obj: dict | ModelType) -> tuple[Callable]:
    if isinstance(compare_obj, dict):

        def extract_value(obj: dict, key: Any) -> Any:
            return obj[key]

        def extract_fields(obj: dict) -> dict:
            return obj

    else:

        def extract_value(obj: ModelType, field: Any) -> Any:
            return getattr(obj, field)

        def extract_fields(obj: ModelType) -> Any:
            return obj.__table__.columns.keys()

    return extract_value, extract_fields
