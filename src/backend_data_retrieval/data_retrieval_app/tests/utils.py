import random
import string
from typing import Any


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


def random_string(length: int = 15):
    """Generates a random string of a specified length (default is 15)."""
    return "".join(
        random.choice(string.ascii_letters) for _ in range(random.randint(1, length))
    )


def random_int(min_val: int = 0, max_val: int = 100):
    """Generates a random integer between min_val and max_val (default is 0 to 100)."""
    return random.randint(min_val, max_val)


def random_float(min_val: float = 0, max_val: float = 100, precision: int = 2):
    """Generates a random float between min_val and max_val (default is 0 to 100)."""
    return round(random.uniform(min_val, max_val), precision)


def random_boolean():
    """Generates a random boolean value (True or False)."""
    return random.choice([True, False])


def random_list_str(max_length: int = 5) -> list[str]:
    """Generates a list with a random number of random string elements (max 5)."""
    return [
        random_string(random.randint(1, 10))
        for _ in range(random.randint(1, max_length))
    ]


def random_dict(max_length: int = 5) -> dict:
    """Generates a random object."""
    dict = {}
    for _ in range(random.randint(1, max_length)):
        dict[random_string(random.randint(1, 10))] = random_string(
            random.randint(1, 10)
        )
    return dict


def random_value_by_type(value: Any) -> Any:
    """Generates a random value based on the data type of the input value."""
    if isinstance(value, bool):
        return random_boolean()
    elif isinstance(value, str):
        return random_string() if value == "" else value
    elif isinstance(value, int):
        return random_int()
    elif isinstance(value, dict):
        return replace_false_values(value)  # Recursively handle nested dictionaries
    return value  # Fallback for other types


def replace_false_values(data: dict) -> dict:
    """
    Recursively replaces all 'false' values (empty string, 0, False, empty list etc.)
    in the dictionary with a random value of the corresponding data type.
    """
    for key, value in data.items():
        # Handle nested dictionaries recursively
        if isinstance(value, dict):
            data[key] = replace_false_values(value)

        # Exclude items here since we add items to the empty list later
        elif isinstance(value, list) and len(value) == 0 and key != "items":
            data[key] = [random_dict()]
        elif isinstance(value, list) and len(value) == 1 and value[0] == "":
            data[key] = random_list_str()
        elif isinstance(value, list):
            data[key] = [
                (
                    replace_false_values(val)
                    if isinstance(val, dict)
                    else (
                        random_value_by_type(val)
                        if val in ("", 0, False, None)
                        else val
                    )
                )
                for val in value
            ]
        # Replace false-like values for simple types
        elif value in ("", 0, False, None):
            data[key] = random_value_by_type(value)

    return data
