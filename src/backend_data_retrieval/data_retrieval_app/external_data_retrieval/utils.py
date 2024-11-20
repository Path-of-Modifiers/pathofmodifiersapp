import time
from collections.abc import Callable
from functools import wraps

from data_retrieval_app.logs.logger import timing_logger as timing_logger


def async_timing_tracker(func: Callable) -> Callable:
    # filepath = os.path.join(
    #    os.path.dirname(__file__),
    #    "timing_data",
    #    func.__name__,
    # )
    # if not os.path.exists(filepath):
    #    os.mkdir(filepath)
    #    n_previous_runs = 0
    # else:
    #    n_previous_runs = len(os.listdir(filepath))
    # filename = filepath + f"/{n_previous_runs}.csv"
    # with open(filename, "x") as infile:
    #    infile.write("start_time,end_time,time_diff\n")

    @wraps(func)
    async def wrap(*args, **kwargs):
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        end_time = time.perf_counter()

        # with open(filename, "a") as infile:
        #     infile.write(
        #         f"{start_time:0.3f},{end_time:0.3f},{end_time-start_time:0.3f}\n"
        #     )

        timing_logger.info(
            f"function={func.__name__} start_time_ms={start_time:0.3f} end_time_ms={end_time:0.3f} time_diff_ms={end_time-start_time:0.3f}"
        )

        return result

    return wrap


def sync_timing_tracker(func: Callable) -> Callable:
    # filepath = os.path.join(
    #    os.path.dirname(__file__),
    #    "timing_data",
    #    func.__name__,
    # )
    # if not os.path.exists(filepath):
    #    os.mkdir(filepath)
    #    n_previous_runs = 0
    # else:
    #    n_previous_runs = len(os.listdir(filepath))
    # filename = filepath + f"/{n_previous_runs}.csv"
    # with open(filename, "x") as infile:
    #    infile.write("start_time,end_time,time_diff\n")

    @wraps(func)
    def wrap(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        # with open(filename, "a") as infile:
        #    infile.write(
        #        f"{start_time:0.3f},{end_time:0.3f},{end_time-start_time:0.3f}\n"
        #    )

        timing_logger.info(
            f"function={func.__name__} start_time={start_time:0.3f} end_time={end_time:0.3f} time_diff={end_time-start_time:0.3f}"
        )

        return result

    return wrap


class ProgramTooSlowException(Exception):
    pass


class ProgramRunTooLongException(Exception):
    pass


class WrongLeagueSetException(Exception):
    pass
