import requests
import time
import logging
import asyncio
import aiohttp
import os
import threading
import pandas as pd
from tqdm import tqdm
from copy import deepcopy
from typing import List, Union, Tuple, Dict, Coroutine, Iterator, Optional
from concurrent.futures import ThreadPoolExecutor, Future

from external_data_retrieval.detectors.unique_detector import (
    UniqueJewelDetector,
    UniqueJewelleryDetector,
    UniqueArmourDetector,
    UniqueWeaponDetector,
    UniqueDetector,
)

from external_data_retrieval.utils import sync_timing_tracker

pd.options.mode.chained_assignment = None  # default='warn'

BASEURL = os.getenv("DOMAIN")
MANUAL_NEXT_CHANGE_ID = os.getenv("MANUAL_NEXT_CHANGE_ID")
NEXT_CHANGE_ID = os.getenv("NEXT_CHANGE_ID")


class APIHandler:
    headers = {
        "User-Agent": "OAuth pathofmodifiers/0.1.0 (contact: ***REMOVED***) StrictMode"
    }

    if "localhost" not in BASEURL:
        base_pom_api_url = f"https://{BASEURL}"
    else:
        base_pom_api_url = "http://src-backend-1"

    def __init__(
        self,
        url: str,
        auth_token: str,
        *,
        logger_parent: logging.Logger,
        n_wanted_items: int = 100,
        n_unique_wanted_items: int = 5,
        item_detectors: List[Union[UniqueDetector]] = [
            UniqueJewelDetector(),
            UniqueJewelleryDetector(),
            UniqueArmourDetector(),
            UniqueWeaponDetector(),
        ],
    ) -> None:
        """
        Parameters:
            :param url: (str) A string containing POE public stash api url.
            :param auth_token: (str) A string containing OAuth2 auth token.
            :param n_wanted_items: (int) The number of items the program should search for before quitting.
            :param n_unique_wanted_items: (int) The number of different type of items the program should search for before quitin.
            :param item_detectors: (List[ItemDetector]) A list of `ItemDetector` instances.
        """
        self.url = url
        self.auth_token = auth_token
        self.headers["Authorization"] = "Bearer " + auth_token

        self.item_detectors = item_detectors

        self.n_found_items = 0
        self.n_wanted_items = n_wanted_items

        self.n_unique_items_found = 0
        self.n_unique_wanted_items = n_unique_wanted_items

        self.logger = logger_parent.getChild("API_handler")

        self.time_for_last_ratelimit = None

    @property
    def recently_ratelimited(self) -> bool:
        """
        To avoid continously running into the rate limit, we want to track
        if we have recently been rate limited. Currently "recently" refers
        to 180 seconds. If we have been recently ratelimited, you can choose
        to act differently, such as adding artificial delay.
        """
        if self.time_for_last_ratelimit is None:
            return False
        elif time.perf_counter() - self.time_for_last_ratelimit > 180:
            return False
        else:
            return True

    def _json_to_df(self, stashes: List) -> pd.DataFrame:
        df_temp = pd.json_normalize(stashes)
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

    def _check_stashes(self, stashes: List) -> pd.DataFrame:
        """
        Parameters:
            :param stashes: (list) A list of stash objects
        """
        df_wanted = pd.DataFrame()
        n_new_items = 0
        n_total_unique_items = 0

        df = self._json_to_df(stashes)

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

                df = df_leftover.copy(deep=True)
        except Exception as e:
            self.logger.critical(
                f"While checking stashes (detector: {item_detector}), the exception below occured:"
            )
            self.logger.critical(e)
            raise e

        # Updates progress bars
        self.n_found_items += n_new_items

        self.n_unique_items_found = n_total_unique_items

        return df_wanted.reset_index()

    def _get_latest_change_id(self) -> str:
        response = requests.get(
            "https://www.pathofexile.com/api/trade/data/change-ids",
            headers={"User-Agent": self.headers["User-Agent"]},
        )
        response.raise_for_status()
        response_json = response.json()
        next_change_id = response_json["psapi"]

        if MANUAL_NEXT_CHANGE_ID:  # For testing purposes, set manual next_change_id
            next_change_id = NEXT_CHANGE_ID

        return next_change_id

    async def _send_n_recursion_requests(
        self,
        n: int,
        session: aiohttp.ClientSession,
        waiting_for_next_id_lock: threading.Lock,
    ) -> List:
        stashes = []  # For exeption handling
        headers = None  # For exeption handling
        if n == 0:
            # End of recursion
            return []

        if self.requests_since_last_checkpoint == 30:
            # End of expedition
            return []
        waiting_for_next_id_lock.acquire()
        try:
            async with session.get(
                self.url, params={"id": self.next_change_id}
            ) as response:
                headers = response.headers
                if response.status >= 300:
                    if response.status == 502:
                        waiting_for_next_id_lock.release()
                        time.sleep(2)
                        return await self._send_n_recursion_requests(
                            n, session, waiting_for_next_id_lock
                        )
                    elif response.status == 429:
                        time.sleep(int(headers["Retry-After"]))
                        waiting_for_next_id_lock.release()
                        return await self._send_n_recursion_requests(
                            n, session, waiting_for_next_id_lock
                        )
                    else:
                        response.raise_for_status()

                new_next_change_id = headers["X-Next-Change-Id"]
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
                    n, session, waiting_for_next_id_lock
                )

                response_json = await response.json()
                stashes += response_json["stashes"]
                del response_json
                return stashes
        except Exception as e:
            print("Exiting '_send_n_recursion_requests' gracefully")
            self.logger.critical(e.with_traceback())
            self.logger.info("Exiting '_send_n_recursion_requests' gracefully")
            if waiting_for_next_id_lock.locked():
                print("Released lock after crash")
                if headers is not None:
                    if (
                        headers["X-Rate-Limit-Ip"].split(":")[0]
                        == headers["X-Rate-Limit-Ip-State"].split(":")[0]
                    ):
                        print("Hit ratelimit, cooling down for one test period.")
                        time.sleep(int(headers["X-Rate-Limit-Ip"].split(":")[1]))

                waiting_for_next_id_lock.release()
            raise e

    async def _follow_stream(
        self,
        stashes_ready_event: threading.Event,
        waiting_for_next_id_lock: threading.Lock,
        stash_lock: threading.Lock,
    ):
        """
        Follows the API stream until conditions are met
        """
        stashes = []  # For exeption handling

        session = aiohttp.ClientSession(headers=self.headers)
        expedition_depth = 30
        try:
            while True:
                while self.requests_since_last_checkpoint < expedition_depth:

                    stashes = await self._send_n_recursion_requests(
                        5, session, waiting_for_next_id_lock
                    )
                    # print(f"Thread {threading.get_ident()} finished 5 requests")
                    stash_lock.acquire()
                    self.stashes += stashes
                    stash_lock.release()
                    del stashes

                stashes = []
                stashes_ready_event.set()
                time.sleep(1)
        except Exception as e:
            self.logger.critical(e)
            raise e
        finally:
            self.logger.info("Exiting '_follow_stream' gracefully.")
            print("Exiting '_follow_stream' gracefully.")

            await session.close()

    def _run_async_follow_stream(
        self,
        stashes_ready_event: threading.Event,
        waiting_for_next_id_lock: threading.Lock,
        stash_lock: threading.Lock,
    ):
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
        df = pd.DataFrame()
        for i in range(n):
            df = self._process_stream(stashes_ready_event, stash_lock, df)

        return df

    def start_data_stream(
        self, executor: ThreadPoolExecutor, listeners: int, has_crashed: bool
    ) -> Dict[Future, str] | Future:
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
        for i in range(listeners):
            future = executor.submit(
                self._run_async_follow_stream,
                stashes_ready_event,
                waiting_for_next_id_lock,
                stash_lock,
            )
            futures[future] = "listener"

        if has_crashed:
            return future
        else:
            return futures

    def dump_stream(
        self, track_progress: bool = True, listeners: int = 2
    ) -> Iterator[pd.DataFrame]:
        """
        The method which begins making API calls and fetching data.

        Parameters:
            :track_progress: (bool) Defaults to True. Currently has no function
        """

        try:
            stashes_ready_event = self.stashes_ready_event
            stash_lock = self.stash_lock
        except AttributeError:
            raise Exception("The method 'start_data_stream' must be called prior")
        else:
            time.sleep(5)
            while True:
                print("Begining processing the stream")
                df = self._gather_n_checkpoints(stashes_ready_event, stash_lock)
                print("Finished processing the stream, entering transformation phase")
                yield df.reset_index()
                del df
                print("Finished transformation phase.")
