import threading
import time
from concurrent.futures import (
    ALL_COMPLETED,
    FIRST_COMPLETED,
    ThreadPoolExecutor,
    wait,
)

import redis
from backend_api.app.core.schemas.league import League
from pydantic import TypeAdapter

from data_retrieval_app.external_data_retrieval.cache import get_cache
from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.external_data_retrieval.data_retrieval.currency_api_handler import (
    CurrencyAPIHandler,
)
from data_retrieval_app.external_data_retrieval.data_retrieval.poe_api_handler import (
    PoEAPIHandler,
)
from data_retrieval_app.external_data_retrieval.transforming_data.transform_poe_api_data import (
    PoEAPIDataTransformer,
)
from data_retrieval_app.external_data_retrieval.utils import (
    ProgramTooSlowException,
)
from data_retrieval_app.logs.logger import external_data_retrieval_logger as logger
from data_retrieval_app.logs.logger import setup_logging
from data_retrieval_app.pom_api_authentication import (
    get_superuser_token_headers,
)
from data_retrieval_app.utils import find_hours_since_launch, get_data_safe


class ContinuousDataRetrieval:
    auth_token = settings.POE_PUBLIC_STASHES_AUTH_TOKEN
    stash_tab_url = "https://api.pathofexile.com/public-stash-tabs"

    backend_base_url = settings.BACKEND_BASE_URL
    active_league_url = f"{backend_base_url}/league/active_league/"
    currency_url = f"{backend_base_url}/currency/"
    pom_auth_headers = get_superuser_token_headers(backend_base_url)

    def __init__(self):
        self.leagues = self._get_leagues()

        self.data_transformer = PoEAPIDataTransformer(self.leagues)

        self.poe_api_handler = PoEAPIHandler(
            url=self.stash_tab_url,
            auth_token=self.auth_token,
            leagues=self.leagues,
        )

        self.currency_api_handler = CurrencyAPIHandler(
            url="https://api.poe.watch/exchange/ratios?league={league}&game=poe1"
        )

    def _get_leagues(self) -> list[League]:
        response = get_data_safe(
            self.active_league_url, headers=self.pom_auth_headers, logger=logger
        )

        return TypeAdapter(list[League]).validate_python(response.json())

    def _follow_data_dump_stream(self, cache: redis.Redis):
        current_hours = find_hours_since_launch(self.leagues)
        # Only need to refer to one league to see when a new hour starts
        current_hour = current_hours[self.leagues[0].leagueId]
        next_hour = current_hour + 1
        logger.info("Retrieving modifiers from db.")
        currencies = self.currency_api_handler.get_currency_data(
            self.leagues, current_hours
        )
        self.data_transformer.set_currencies(currencies)
        self.data_transformer.set_current_hours(current_hours)
        iter_data = self.poe_api_handler.dump_stream(cache)
        while current_hour < next_hour:
            organized_items, next_change_id = next(iter_data)
            self.data_transformer.transform_and_insert(organized_items)
            if next_change_id is not None:
                # Only set the next change id once the data has been safely inserted
                cache.set("next_change_id", next_change_id)

            current_hours = find_hours_since_launch(self.leagues)
            current_hour = current_hours[self.leagues[0].leagueId]

        self.data_transformer.end_of_hour_cleanup()

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
            self.leagues = self._get_leagues()

        with ThreadPoolExecutor(
            max_workers=max_workers
        ) as executor, get_cache() as cache:
            futures = {}
            futures.update(
                self.poe_api_handler.initialize_data_stream_threads(
                    max_workers - 1, executor, reset_event, stop_event, cache
                )
            )
            follow_future = executor.submit(self._follow_data_dump_stream, cache)
            futures[follow_future] = "data_processing"
            logger.info("Waiting for futures to crash.")
            finished = False
            while True:
                if finished:
                    return

                done_futures, _ = wait(futures, return_when=FIRST_COMPLETED)
                while done_futures:
                    future = done_futures.pop()
                    future_job: str = futures.pop(future)
                    if future_job == "data_processing":
                        try:
                            future.result()
                            stop_event.set()
                            wait(futures, return_when=ALL_COMPLETED)
                            finished = True
                        except ProgramTooSlowException:
                            logger.info(
                                f"The job '{future_job}' was too slow. Restarting..."
                            )
                            stop_event.set()

                            wait(futures, return_when=ALL_COMPLETED)

                            finished = True
                        except Exception:
                            logger.exception(
                                f"The following exception occured in job '{future_job}'",
                            )
                            # reset to the latest change id checkpoint
                            reset_event.set()
                            follow_future = executor.submit(
                                self._follow_data_dump_stream, cache
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
