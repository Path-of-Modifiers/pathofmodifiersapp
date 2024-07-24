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
from concurrent.futures import ThreadPoolExecutor, as_completed

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

    async def _start_listening_pool(
        self,
        loop: asyncio.AbstractEventLoop,
        listeners: int,
        stashes_ready_event: threading.Event,
        waiting_for_next_id_lock: threading.Lock,
        stash_lock: threading.Lock,
    ):
        session = aiohttp.ClientSession(headers=self.headers)

        expedition_depth = 30
        try:
            with ThreadPoolExecutor(max_workers=listeners) as executor:
                futures = [
                    executor.submit(asyncio.set_event_loop, loop)
                    for i in range(listeners)
                ]
                for future in as_completed(futures):
                    future.result()
                while True:
                    futures = []
                    for i in range(expedition_depth):
                        future = loop.run_in_executor(
                            executor,
                            self._send_request,
                            session,
                            waiting_for_next_id_lock,
                        )
                        futures.append(future)

                    # stashes = []
                    # for future in as_completed(futures):
                    #     stashes += future.result()

                    stashes = await asyncio.gather(*futures)

                    stash_lock.acquire()
                    self.stashes = stashes
                    stash_lock.release()

                    stashes_ready_event.set()

        finally:
            await session.close()

    def _run_async_start_listening_pool(
        self,
        listeners: int,
        stashes_ready_event: threading.Event,
        waiting_for_next_id_lock: threading.Lock,
        stash_lock: threading.Lock,
    ):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        asyncio.run(
            self._start_listening_pool(
                loop,
                listeners,
                stashes_ready_event,
                waiting_for_next_id_lock,
                stash_lock,
            )
        )

    async def _send_request(
        self,
        session: aiohttp.ClientSession,
        waiting_for_next_id_lock: threading.Lock,
    ) -> List:
        print(f"Thread {threading.get_ident()} acquired lock.")
        waiting_for_next_id_lock.acquire()
        async with session.get(
            self.url, params={"id": self.next_change_id}
        ) as response:
            headers = response.headers
            if response.status >= 300:
                if response.status == 502:
                    waiting_for_next_id_lock.release()
                    time.sleep(2)
                    stashes = await self._send_request(
                        session, waiting_for_next_id_lock
                    )
                    return stashes
                response.raise_for_status()

            new_next_change_id = headers["X-Next-Change-Id"]
            self.next_change_id = new_next_change_id

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

            response_json = await response.json()
            stashes += response_json["stashes"]
            del response_json

        return stashes

    def _run_async_send_request(self, *args, **kwargs) -> List:
        future = asyncio.run(self._send_request(*args, **kwargs))
        return future

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

        print("Copied stashes locally and reset the event.")
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

    def dump_stream(
        self, track_progress: bool = True, listeners: int = 2
    ) -> Iterator[pd.DataFrame]:
        """
        The method which begins making API calls and fetching data.

        Parameters:
            :track_progress: (bool) Defaults to True. Currently has no function
        """
        stashes_ready_event = threading.Event()
        waiting_for_next_id_lock = threading.Lock()
        stash_lock = threading.Lock()

        self.next_change_id = self._get_latest_change_id()
        self.requests_since_last_checkpoint = 0
        self.stashes = []

        thread = threading.Thread(
            target=self._run_async_start_listening_pool,
            args=(listeners, stashes_ready_event, waiting_for_next_id_lock, stash_lock),
        )
        print("Starting listening pool thread")
        thread.start()
        print("Finished starting listening pool thread")
        time.sleep(5)
        while True:
            print("Begining processing the stream")
            df = self._gather_n_checkpoints(stashes_ready_event, stash_lock)
            print("Finished processing the stream, entering transformation phase")
            yield df.reset_index()
            del df
