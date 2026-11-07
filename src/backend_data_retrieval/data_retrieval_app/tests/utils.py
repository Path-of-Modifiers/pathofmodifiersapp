import random
import string
from typing import Any

RNG = random.Random()


def random_lower_string(
    *,
    small_string: bool | None = None,
    rng: random.Random = RNG,
) -> str:
    """Generate a random lowercase string.

    Args:
        small_string (bool | None): Optional whether to have small string. Defaults to None.

    Returns:
        str: Random lowercase string.
    """
    random_lower_string = "".join(rng.choices(string.ascii_lowercase, k=32))
    if small_string:
        random_lower_string = random_lower_string[:5]
    return random_lower_string


def random_string(
    max_length: int = 15,
    rng: random.Random = RNG,
):
    """Generates a random string of a specified length (default is 15)."""
    return "".join(
        rng.choice(string.ascii_letters)
        for _ in range(random_int(5, max_length, rng=rng))
    )


def random_int(min_val: int = 1, max_val: int = 100, *, rng: random.Random = RNG):
    """Generates a random integer between min_val and max_val (default is 0 to 100)."""
    return rng.randint(min_val, max_val)


def random_float(
    min_val: float = 1,
    max_val: float = 100,
    precision: int = 2,
    *,
    rng: random.Random = RNG,
):
    """Generates a random float between min_val and max_val (default is 0 to 100)."""
    return round(rng.uniform(min_val, max_val), precision)


def random_boolean(*, rng: random.Random = RNG):
    """Generates a random boolean value (True or False)."""
    return rng.choice([True, False])


def random_list_str(max_length: int = 5, *, rng: random.Random = RNG) -> list[str]:
    """Generates a list with a random number of random string elements (max 5)."""
    return [random_string(rng=rng) for _ in range(random_int(5, max_length, rng=rng))]


def random_dict(max_length: int = 5, *, rng: random.Random = RNG) -> dict:
    """Generates a random object."""
    dict = {}
    for _ in range(random_int(1, max_length, rng=rng)):
        dict[random_string(rng=rng)] = random_string(rng=rng)
    return dict


def random_value_by_type(
    annotation: Any, *, rng: random.Random = RNG, field_name: str = ""
) -> Any:
    """Generates a random value based on the data type of the input value."""
    if annotation is bool:
        return random_boolean(rng=rng)
    elif annotation is str:
        return random_string(rng=rng)
    elif annotation is int:
        return random_int(rng=rng)
    raise TypeError(
        f"No generator registered for {annotation!r} " f"(field={field_name!r})"
    )


def replace_false_values(data: dict) -> dict:
    """
    Recursively replaces all 'false' values (empty string, 0, False, empty list etc.)
    in the dictionary with a random value of the corresponding data type.
    """
    for key, value in data.items():
        # Handle nested dictionaries recursively
        if isinstance(value, dict):
            data[key] = replace_false_values(value)
        elif key == "identified":
            continue
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
