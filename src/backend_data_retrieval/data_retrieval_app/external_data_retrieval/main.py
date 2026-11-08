import signal
import threading
import time
from concurrent.futures import (
    FIRST_COMPLETED,
    ThreadPoolExecutor,
    wait,
)

import redis

from data_retrieval_app.external_data_retrieval.cache import get_cache
from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.external_data_retrieval.data_retrieval.currency_api_handler import (
    CurrencyAPIHandler,
)
from data_retrieval_app.external_data_retrieval.data_retrieval.poe_api_handler import (
    PoEAPIHandler,
)
from data_retrieval_app.external_data_retrieval.utils import (
    ProgramTooSlowException,
)
from data_retrieval_app.logs.logger import external_data_retrieval_logger as logger
from data_retrieval_app.logs.logger import setup_logging
from data_retrieval_app.pom_api_authentication import (
    get_superuser_token_headers,
)
from data_retrieval_app.utils import (
    find_hours_since_launch,
    get_leagues_active,
)


class ContinuousDataRetrieval:
    auth_token = settings.POE_PUBLIC_STASHES_AUTH_TOKEN
    stash_tab_url = "https://api.pathofexile.com/public-stash-tabs"

    backend_base_url = settings.BACKEND_BASE_URL
    currency_url = f"{backend_base_url}/currency/"
    pom_auth_headers = get_superuser_token_headers(backend_base_url)

    def __init__(self):
        self.leagues = get_leagues_active(self.pom_auth_headers)

        self.poe_api_handler = PoEAPIHandler(
            url=self.stash_tab_url,
            auth_token=self.auth_token,
            leagues=self.leagues,
        )

        self.currency_api_handler = CurrencyAPIHandler(
            url="https://api.poe.watch/exchange/ratios?league={league}&game=poe1"
        )

    def _follow_data_dump_stream(self, cache: redis.Redis, stop_event: threading.Event):
        current_hours = find_hours_since_launch(self.leagues)
        # Only need to refer to one league to see when a new hour starts
        current_hour = current_hours[self.leagues[0].leagueId]
        next_hour = current_hour + 1
        currencies = self.currency_api_handler.get_currency_data(
            self.leagues, current_hours
        )
        iter_data = self.poe_api_handler.dump_stream(
            cache, current_hours, currencies, stop_event
        )
        while current_hour < next_hour:
            next_change_id = next(iter_data, None)
            if next_change_id is None:
                break
            # Only set the next change id once the data has been safely inserted
            cache.set("next_change_id", next_change_id)

            current_hours = find_hours_since_launch(self.leagues)
            current_hour = current_hours[self.leagues[0].leagueId]
        else:
            # only occurs during natural end to the while loop
            self.poe_api_handler.end_of_hour_cleanup()

    def _handle_shutdown(
        self, stop_event: threading.Event, executor: ThreadPoolExecutor
    ):
        logger.info("Received termination signal, exiting gracefully...")
        stop_event.set()
        executor.shutdown(wait=True, cancel_futures=True)
        self.poe_api_handler.end_of_program_cleanup()
        logger.info("Exited data retrieval gracefully")

    def retrieve_data(self):
        logger.info("Program starting up.")
        logger.info("Initiating data stream.")
        max_workers = 3
        reset_event = threading.Event()
        stop_event = threading.Event()

        # leagues is empty = no active leagues. Thus sleep
        while not self.leagues:
            logger.warning("Found no active leagues, sleeping for 5 min.")
            time.sleep(300)
            self.leagues = get_leagues_active(self.pom_auth_headers)

        with ThreadPoolExecutor(
            max_workers=max_workers
        ) as executor, get_cache() as cache:
            signal.signal(
                signal.SIGTERM,
                lambda signum, frame: self._handle_shutdown(stop_event, executor),
            )
            signal.signal(
                signal.SIGINT,
                lambda signum, frame: self._handle_shutdown(stop_event, executor),
            )
            # cache.flushdb()
            futures = {}
            futures.update(
                self.poe_api_handler.initialize_data_stream_threads(
                    max_workers - 1, executor, reset_event, stop_event, cache
                )
            )
            follow_future = executor.submit(
                self._follow_data_dump_stream, cache, stop_event
            )
            futures[follow_future] = "data_processing"
            logger.info("Waiting for futures to crash.")
            finished = False
            while not stop_event.is_set():
                if finished:
                    return

                done_futures, _ = wait(futures, return_when=FIRST_COMPLETED)
                while done_futures and not finished and not stop_event.is_set():
                    future = done_futures.pop()
                    future_job: str = futures.pop(future)
                    if future_job == "data_processing":
                        try:
                            future.result()
                            finished = True
                        except ProgramTooSlowException:
                            logger.info(
                                f"The job '{future_job}' was too slow. Restarting..."
                            )
                            finished = True
                        except Exception:
                            logger.exception(
                                f"The following exception occured in job '{future_job}'",
                            )
                            # reset to the latest change id checkpoint
                            reset_event.set()
                            follow_future = executor.submit(
                                self._follow_data_dump_stream, cache, stop_event
                            )
                            futures[follow_future] = "data_processing"
                    elif future_job.startswith("listener"):
                        listener_id = int(future_job[-1])
                        try:
                            future.result()
                        except Exception:
                            logger.exception(
                                f"The following exception occured in listener {listener_id}"
                            )
                        if stop_event.is_set():
                            continue

                        futures.update(
                            self.poe_api_handler.initialize_data_stream_threads(
                                max_workers - 1,
                                executor,
                                reset_event,
                                stop_event,
                                cache,
                                crashed=True,
                                listener_id=listener_id,
                            )
                        )


def main():
    logger.info("Starting the program...")
    setup_logging()

    data_retriever = ContinuousDataRetrieval()
    data_retriever.retrieve_data()


if __name__ == "__main__":
    main()
