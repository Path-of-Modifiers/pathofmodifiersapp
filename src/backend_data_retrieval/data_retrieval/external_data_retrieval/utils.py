from typing import Callable
from functools import wraps
import time
import os


def async_timing_tracker(func: Callable) -> Callable:
    filepath = os.path.join(
        os.path.dirname(__file__),
        "timing_data",
        func.__name__,
    )
    if not os.path.exists(filepath):
        os.mkdir(filepath)
        n_previous_runs = 0
    else:
        n_previous_runs = len(os.listdir(filepath))
    filename = filepath + f"/{n_previous_runs}.csv"
    with open(filename, "x") as infile:
        infile.write("start_time,end_time,time_diff\n")

    @wraps(func)
    async def wrap(*args, **kwargs):
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        end_time = time.perf_counter()

        with open(filename, "a") as infile:
            infile.write(
                f"{start_time:0.3f},{end_time:0.3f},{end_time-start_time:0.3f}\n"
            )

        return result

    return wrap


def sync_timing_tracker(func: Callable) -> Callable:
    filepath = os.path.join(
        os.path.dirname(__file__),
        "timing_data",
        func.__name__,
    )
    if not os.path.exists(filepath):
        os.mkdir(filepath)
        n_previous_runs = 0
    else:
        n_previous_runs = len(os.listdir(filepath))
    filename = filepath + f"/{n_previous_runs}.csv"
    with open(filename, "x") as infile:
        infile.write("start_time,end_time,time_diff\n")

    @wraps(func)
    def wrap(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        with open(filename, "a") as infile:
            infile.write(
                f"{start_time:0.3f},{end_time:0.3f},{end_time-start_time:0.3f}\n"
            )

        return result

    return wrap


class ProgramTooSlowException(Exception):
    pass


class ProgramRunTooLongException(Exception):
    pass
