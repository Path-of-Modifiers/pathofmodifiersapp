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

from external_data_retrieval.detectors.unique_detector import (
    UniqueJewelDetector,
    UniqueJewelleryDetector,
    UniqueArmourDetector,
    UniqueWeaponDetector,
    UniqueDetector,
)

from external_data_retrieval.utils import async_timing_tracker

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

        return df_wanted

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

    def _initialize_stream(self) -> Tuple[str, List]:
        """
        Makes an initial, synchronous, API call.
        """
        next_change_id = self._get_latest_change_id()

        response = requests.get(
            self.url, headers=self.headers, params={"id": next_change_id}
        )
        if response.status_code >= 300:
            if response.status_code == 429:
                # https://www.pathofexile.com/developer/docs/index#ratelimits
                # Rate limits are dynamic
                headers = response.headers
                retry_after = int(headers["Retry-After"])
                time.sleep(retry_after + 1)
                self.logger.info("Encountered a ratelimit.")
                return self._initialize_stream(next_change_id=next_change_id)

            response.raise_for_status()
        response_json = response.json()

        stashes = response_json["stashes"]
        if stashes:
            next_change_id = response_json["next_change_id"]

        return next_change_id, stashes

    async def _start_next_N_request(
        self, session: aiohttp.ClientSession, next_change_id: str, N: int
    ) -> Tuple[List, str]:
        print(N)
        if self.recently_ratelimited:
            # Adds artificial delay if we have recently been ratelimited
            time.sleep(1)

        if N == 0:
            return [], next_change_id

        async with session.get(self.url, params={"id": next_change_id}) as response:
            headers = response.headers
            if response.status >= 300:
                if response.status == 429:
                    # https://www.pathofexile.com/developer/docs/index#ratelimits
                    # Rate limits are dynamic
                    retry_after = int(headers["Retry-After"])
                    self.time_for_last_ratelimit = time.perf_counter()
                    await asyncio.sleep(retry_after + 1)
                    return await self._start_next_N_request(session, next_change_id, N)

                else:
                    response.raise_for_status()

            new_next_change_id = headers["X-Next-Change-Id"]
            if new_next_change_id == next_change_id:
                time.sleep(
                    120
                )  # Waits 120 seconds before continuing to pursue the stream
            else:
                next_change_id = new_next_change_id
                N -= 1

            stashes, next_change_id = await self._start_next_N_request(
                session, next_change_id, N
            )

            response_json = await response.json()
            stashes += response_json["stashes"]

        return stashes, next_change_id

    def _run_async_follow_stream(self, stashes_lock: threading.Lock):
        asyncio.run(self._follow_stream(stashes_lock))

    @async_timing_tracker
    async def _start_new_mini_expedition(
        self, session: aiohttp.ClientSession, next_change_id: str, expedition_depth: int
    ) -> str:
        stashes, next_change_id = await self._start_next_N_request(
            session, next_change_id=next_change_id, N=expedition_depth
        )

        self.stashes += stashes

        return next_change_id

    async def _follow_stream(self, stashes_lock: threading.Lock):
        """
        Follows the API stream until conditions are met
        """
        stashes_lock.acquire()
        print("Locked the stashes inside follow_stream.")
        next_change_id, new_stashes = self._initialize_stream()

        self.stashes = new_stashes

        session = aiohttp.ClientSession(headers=self.headers)
        try:
            while True:

                next_change_id = await self._start_new_mini_expedition(
                    session, next_change_id=next_change_id, expedition_depth=30
                )

                stashes_lock.release()
                time.sleep(1)
                stashes_lock.acquire()
        finally:
            await session.close()

    def _process_stream(self, stashes_lock: threading.Lock) -> pd.DataFrame:
        df = pd.DataFrame()
        for i in range(10):
            stashes_lock.acquire()
            print("Locked the stashes inside process_stream.")
            stashes_local = self.stashes
            del self.stashes
            self.stashes = []
            stashes_lock.release()
            print("Released the stashes lock inside pocess_stream.")
            wandted_df = self._check_stashes(stashes_local)
            df = pd.concat((df, wandted_df))
            print("Finished processing the data, waiting for more.")
        return df

    def dump_stream(self, track_progress: bool = True) -> Iterator[pd.DataFrame]:
        """
        The method which begins making API calls and fetching data.

        Parameters:
            :track_progress: (bool) Defaults to True. Currently has no function
        """
        stashes_lock = threading.Lock()

        print("Initializing follow stream thread")
        follow_stream_thread = threading.Thread(
            target=self._run_async_follow_stream, args=(stashes_lock,)
        )
        print("Starting follow stream thread")
        follow_stream_thread.start()
        print("Finished starting thread")
        time.sleep(5)
        while True:
            print("Begining processing the stream")
            df = self._process_stream(stashes_lock)
            print("Finished processing the stream, entering transformation phase")
            yield df.reset_index()
            del df
