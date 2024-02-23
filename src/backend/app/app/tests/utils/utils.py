import random
import string
from typing import Optional
from datetime import datetime, timedelta


def random_lower_string(*, small_string: Optional[bool] = None) -> str:
    random_lower_string = "".join(random.choices(string.ascii_lowercase, k=32))
    if small_string:
        random_lower_string = random_lower_string[:5]
    return random_lower_string


def random_int(
    *, small_int: Optional[bool] = None, negative: Optional[bool] = None
) -> int:
    random_int = random.randint(1, 10**32)
    if small_int:
        random_int = random.randint(1, 32767)
    if negative:
        random_int = random_int * -1
    return random_int


def random_float(
    *, small_float: Optional[bool] = None, negative: Optional[bool] = None
) -> float:
    random_float = random.uniform(1, 10**32)
    if small_float:
        random_float = random.uniform(1, 32767)
    if negative:
        random_float = random_float * -1
    return random_float


def random_bool() -> bool:
    return random.choice([True, False])


def random_json():
    return {
        "random_lower_string": random_lower_string(),
        "random_int": random_int(),
        "random_float": random_float(),
        "random_bool": random_bool(),
    }


def random_url():
    return f"https://{random_lower_string()}.{random_lower_string(small_string=True)}"


def random_datetime():
    return datetime.now() + random.uniform(-5, 5) * timedelta(days=1)


def main():
    print(random_lower_string())
    print(random_int())
    print(random_float())
    print(random_bool())
    print(random_url())


if __name__ == "__main__":
    main()
