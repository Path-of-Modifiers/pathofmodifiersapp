import asyncio
import threading
import time
from collections.abc import Iterator
from concurrent.futures import Future, ThreadPoolExecutor

import aiohttp
import pandas as pd
import requests

from external_data_retrieval.config import settings
from external_data_retrieval.detectors.unique_detector import (
    UniqueArmourDetector,
    UniqueDetector,
    UniqueJewelDetector,
    UniqueJewelleryDetector,
    UniqueWeaponDetector,
)
from external_data_retrieval.utils import (
    ProgramRunTooLongException,
    ProgramTooSlowException,
    WrongLeagueSetException,
    sync_timing_tracker,
)
from logs.logger import data_retrieval_logger as logger

pd.options.mode.chained_assignment = None  # default='warn'


class APIHandler:
    headers = {
        "User-Agent": f"OAuth pathofmodifiers/0.1.0 (contact: {settings.OATH_ACC_TOKEN_CONTACT_EMAIL}) StrictMode"
    }

    if "localhost" not in settings.BASEURL:
        base_pom_api_url = f"https://{settings.BASEURL}"
    else:
        base_pom_api_url = "http://src-backend-1"

    def __init__(
        self,
        url: str,
        auth_token: str,
        *,
        n_wanted_items: int = 100,
        n_unique_wanted_items: int = 5,
        item_detectors: list[UniqueDetector] | None = None,
    ) -> None:
        """
        Parameters:
            :param url: (str) A string containing POE public stash api url.
            :param auth_token: (str) A string containing OAuth2 auth token.
            :param n_wanted_items: (int) The number of items the program should search for before quitting.
            :param n_unique_wanted_items: (int) The number of different type of items the program should search for before quitin.
            :param item_detectors: (list[ItemDetector]) A list of `ItemDetector` instances.
        """
        if item_detectors is None:
            item_detectors = [
                UniqueArmourDetector(),
                UniqueJewelDetector(),
                UniqueJewelleryDetector(),
                UniqueWeaponDetector(),
            ]
        self.url = url
        self.auth_token = auth_token
        self.headers["Authorization"] = "Bearer " + auth_token

        self.item_detectors = item_detectors

        self.n_found_items = 0
        self.n_wanted_items = n_wanted_items

        self.n_unique_items_found = 0
        self.n_unique_wanted_items = n_unique_wanted_items

        self._program_too_slow = False
        self.time_of_launch = time.perf_counter()

    def _json_to_df(self, stashes: list) -> pd.DataFrame:
        df_temp = pd.json_normalize(stashes)
        if "items" not in df_temp.columns:
            return None
        df_temp = df_temp.explode(["items"])
        df_temp = df_temp.loc[~df_temp["items"].isnull()]
        df_temp.drop("items", axis=1, inplace=True)
        df_temp.rename(columns={"id": "stashId"}, inplace=True)

        df = pd.json_normalize(stashes, record_path=["items"])
        df["stash_index"] = df_temp.index

        df_temp.index = df.index
        df[df_temp.columns.to_list()] = df_temp
        df.rename(columns={"id": "gameItemId"}, inplace=True)

        return df

    def _check_stashes(self, stashes: list) -> pd.DataFrame:
        """
        Parameters:
            :param stashes: (list) A list of stash objects
        """
        df_wanted = pd.DataFrame()
        n_new_items = 0
        n_total_unique_items = 0

        df = self._json_to_df(stashes)
        if df is None:
            return df_wanted

        # The stashes are fed to all item detectors, slowly being filtered down
        try:
            for item_detector in self.item_detectors:
                (
                    df_filtered,
                    item_count,
                    n_unique_found_items,
                    df_leftover,
                ) = item_detector.iterate_stashes(df)

                df_wanted = pd.concat((df_wanted, df_filtered))
                n_new_items += item_count
                n_total_unique_items += n_unique_found_items
                if df_leftover.empty:
                    break

                df = df_leftover.copy(deep=True)
        except:
            logger.exception(
                f"While checking stashes (detector: {item_detector}), the exception below occured:"
            )
            raise

        # Updates progress bars
        self.n_found_items += n_new_items

        self.n_unique_items_found = n_total_unique_items

        if df_wanted.empty:
            raise WrongLeagueSetException

        return df_wanted.reset_index()

    def _get_latest_change_id(self) -> str:
        """
        Gets the latest change id from GGG or uses a manual one.
        The change id provided by GGG does not become available in the stream
        before 5 minutes. A manual next change id circumvents this wait.
        """

        if (
            settings.MANUAL_NEXT_CHANGE_ID
        ):  # For testing purposes, set manual next_change_id
            next_change_id = settings.NEXT_CHANGE_ID
            return next_change_id
        response = requests.get(
            "https://www.pathofexile.com/api/trade/data/change-ids",
            headers=self.headers,
        )
        response.raise_for_status()
        response_json = response.json()
        next_change_id = response_json["psapi"]
        time.sleep(
            310
        )  # Sleeps for 5 minutes and 10 seconds (for safety) for the latest change id to be populated

        return next_change_id

    async def _send_n_recursion_requests(
        self,
        n: int,
        session: aiohttp.ClientSession,
        waiting_for_next_id_lock: threading.Lock,
        mini_batch_size: int,
    ) -> list:
        """
        Because we are restricted by the `next_change_id`, queueing get requests is non trivial.
        We therefore send a non-blocking get request and retrieve the `next_change_id` from the headers
        and immediately send another request, without waiting for the response body. This is repeated
        `n` times before finally waiting for the response body.

        The `waiting_for_next_id_lock` is required to make any request.
        """
        headers = None  # For exeption handling
        if n == 0:
            # End of recursion
            return []

        if self.requests_since_last_checkpoint == mini_batch_size:
            # End of batch
            return []
        if self._program_too_slow:
            raise ProgramTooSlowException
        waiting_for_next_id_lock.acquire()
        try:
            async with session.get(
                self.url, params={"id": self.next_change_id}
            ) as response:
                headers = response.headers
                if response.status >= 300:
                    if response.status == 429:
                        logger.critical("Recieved a 429 (ratelimited) response")
                        print(headers)
                        time.sleep(int(headers["Retry-After"]))
                        waiting_for_next_id_lock.release()
                        return await self._send_n_recursion_requests(
                            n, session, waiting_for_next_id_lock, mini_batch_size
                        )
                    else:
                        waiting_for_next_id_lock.release()
                        logger.critical(f"Recieved the response code {response.status}")
                        response.raise_for_status()
                        logger.critical(
                            "The above response code did not result in an error, discarding the response for safety"
                        )
                        return []

                new_next_change_id = headers["X-Next-Change-Id"]
                if new_next_change_id == self.next_change_id:
                    logger.info("We sucessfully caught up to the stream!")
                    time.sleep(
                        30
                    )  # We have caught up to the stream, sleep for 30 seconds to fall behind.
                # print(
                #     f"Thread {threading.get_ident()} acquired lock. Current id={self.next_change_id}, next id={new_next_change_id}"
                # )
                self.next_change_id = new_next_change_id

                self.requests_since_last_checkpoint += 1
                n -= 1
                # print(
                #     f"New id ready, releasing lock. Current request count = {self.requests_since_last_checkpoint}"
                # )
                if (
                    headers["X-Rate-Limit-Ip"].split(":")[0]
                    == headers["X-Rate-Limit-Ip-State"].split(":")[0]
                ):
                    print("Hit ratelimit, cooling down for one test period.")
                    time.sleep(int(headers["X-Rate-Limit-Ip"].split(":")[1]))
                waiting_for_next_id_lock.release()

                stashes = await self._send_n_recursion_requests(
                    n, session, waiting_for_next_id_lock, mini_batch_size
                )

                response_json = await response.json()
                stashes += response_json["stashes"]
                del response_json
                return stashes
        except:
            print("Exiting '_send_n_recursion_requests' gracefully")
            logger.exception(
                "The following exception occured during '_send_n_recursion_requests'"
            )
            logger.info("Exiting '_send_n_recursion_requests' gracefully")
            if waiting_for_next_id_lock.locked():
                logger.info("Released lock after crash")
                if headers is not None:
                    if (
                        "X-Rate-Limit-Ip" in headers.keys()
                        and "X-Rate-Limit-Ip-State" in headers.keys()
                    ):
                        if (
                            headers["X-Rate-Limit-Ip"].split(":")[0]
                            == headers["X-Rate-Limit-Ip-State"].split(":")[0]
                        ):
                            print("Hit ratelimit, cooling down for one test period.")
                            time.sleep(int(headers["X-Rate-Limit-Ip"].split(":")[1]))

                waiting_for_next_id_lock.release()
            raise

    async def _follow_stream(
        self,
        stashes_ready_event: threading.Event,
        waiting_for_next_id_lock: threading.Lock,
        stash_lock: threading.Lock,
    ):
        """
        Follows the API stream for 30 requests before letting another thread take
        the stashes. Sends 5 requets before waiting to recieve the request body.
        """
        stashes = []  # For exeption handling

        timeout = aiohttp.ClientTimeout(total=60)
        session = aiohttp.ClientSession(headers=self.headers, timeout=timeout)
        mini_batch_size = 30
        try:
            while True:
                while self.requests_since_last_checkpoint < mini_batch_size:
                    stashes = await self._send_n_recursion_requests(
                        5, session, waiting_for_next_id_lock, mini_batch_size
                    )
                    # print(f"Thread {threading.get_ident()} finished 5 requests")
                    stash_lock.acquire()
                    self.stashes += stashes
                    stash_lock.release()
                    del stashes

                stashes = []
                stashes_ready_event.set()
                time.sleep(1)
        except:
            logger.exception("The following exception occured during '_follow_stream'")
            raise
        finally:
            logger.info("Exiting '_follow_stream' gracefully.")
            print("Exiting '_follow_stream' gracefully.")

            await session.close()

    def _run_async_follow_stream(
        self,
        stashes_ready_event: threading.Event,
        waiting_for_next_id_lock: threading.Lock,
        stash_lock: threading.Lock,
    ):
        """
        Needed to run an async function from a submit call.
        """
        asyncio.run(
            self._follow_stream(
                stashes_ready_event, waiting_for_next_id_lock, stash_lock
            )
        )

    @sync_timing_tracker
    def _process_stream(
        self,
        stashes_ready_event: threading.Event,
        stash_lock: threading.Lock,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Waits for stashes to be ready (a mini batch), copies them over to the local scope
        of the method, deletes the stashes stored in the class instance,
        and resets the internal mini batch counter.

        Then checks the stashes (filters them).
        """

        stashes_ready_event.wait()
        stash_lock.acquire()

        print("Stashes are ready for processing.")
        stashes_local = self.stashes
        del self.stashes
        self.stashes = []

        self.requests_since_last_checkpoint = 0
        stash_lock.release()
        stashes_ready_event.clear()

        # print("Copied stashes locally and reset the event.")
        wandted_df = self._check_stashes(stashes_local)
        df = pd.concat((df, wandted_df))
        print("Finished processing the data, waiting for more.")
        return df

    def _gather_n_checkpoints(
        self,
        stashes_ready_event: threading.Event,
        stash_lock: threading.Lock,
        n: int = 10,
    ) -> pd.DataFrame:
        """
        The data collecting is divided into mini batches and batches.
        A batch size is determined by n, and the mini batch size (currently hard coded to be 30).
        """
        df = pd.DataFrame()
        for _ in range(n):
            start_time = time.perf_counter()
            df = self._process_stream(stashes_ready_event, stash_lock, df)
            end_time = time.perf_counter()

            time_per_mini_batch = end_time - start_time
            if time_per_mini_batch > (2 * 60):
                # Does not allow a batch to take longer than 2 minutes
                raise ProgramTooSlowException

        return df

    def set_program_too_slow(self):
        """
        Used to forceall threads to crash, letting the program shut down.
        This method should not be used unless `self.dump_stream` has raised a `ProgramTooSlowException`
        """
        self._program_too_slow = True

    def initialize_data_stream_threads(
        self, executor: ThreadPoolExecutor, listeners: int, has_crashed: bool
    ) -> dict[Future, str] | Future:
        """
        Creates the communication tools between threads and store them for later use.
        Gets the latest change id, and initializes the listeners.

        If `has_crashed` is True, these communication tools are not recreated, but reused.
        """
        if not has_crashed:
            stashes_ready_event = threading.Event()
            waiting_for_next_id_lock = threading.Lock()
            stash_lock = threading.Lock()

            self.stashes_ready_event = stashes_ready_event
            self.waiting_for_next_id_lock = waiting_for_next_id_lock
            self.stash_lock = stash_lock

            self.next_change_id = self._get_latest_change_id()
            self.requests_since_last_checkpoint = 0
            self.stashes = []

        else:
            stashes_ready_event = self.stashes_ready_event
            waiting_for_next_id_lock = self.waiting_for_next_id_lock
            stash_lock = self.stash_lock

        print("Initializing follow stream threads")
        futures = {}
        for _ in range(listeners):
            future = executor.submit(
                self._run_async_follow_stream,
                stashes_ready_event,
                waiting_for_next_id_lock,
                stash_lock,
            )
            futures[future] = "listener"

        if has_crashed:
            if len(futures) == 1:
                return future
            else:
                return futures.keys()
        else:
            return futures

    def dump_stream(self, track_progress: bool = True) -> Iterator[pd.DataFrame]:
        """
        The method uses premad thread communication tools, which requires `start_data_stream` to have been called previously.

        Parameters:
            :track_progress: (bool) Defaults to True. Currently has no function
        """

        try:
            stashes_ready_event = self.stashes_ready_event
            stash_lock = self.stash_lock
        except AttributeError:
            raise Exception("The method 'start_data_stream' must be called prior")
        else:
            time.sleep(5)  # Waits for the listening threads to have time to start up.
            while True:
                print("Begining processing the stream")
                df = self._gather_n_checkpoints(stashes_ready_event, stash_lock)
                print("Finished processing the stream, entering transformation phase")
                yield df.reset_index()
                del df
                print("Finished transformation phase.")
                current_time = time.perf_counter()
                time_since_launch = current_time - self.time_of_launch
                if time_since_launch > 3600:
                    raise ProgramRunTooLongException
