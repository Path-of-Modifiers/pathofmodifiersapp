import requests
import time
import json
import asyncio
import aiohttp
from tqdm import tqdm
from datetime import datetime
from typing import List, Union, Tuple, Dict, Coroutine

from app.external_data_retrieval.detectors.unique_detector import (
    UniqueJewelDetector,
    UniqueDetector,
)


class APIHandler:
    headers = {
        "User-Agent": "OAuth pathofmodifiers/0.1.0 (contact: ***REMOVED***) StrictMode"
    }

    def __init__(
        self,
        url: str,
        auth_token: str,
        n_wanted_items: int = 100,
        n_unique_wanted_items: int = 5,
        item_detectors: List[Union[UniqueDetector]] = [UniqueJewelDetector()],
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

    def _check_stashes(self, stashes: list) -> List[List[Dict[str, str]]]:
        """
        Parameters:
            :param stashes: (list) A list of stash objects
        """
        wanted_stashes = []
        n_new_items = 0
        n_total_unique_items = 0

        # The stashes are fed to all item detectors, slowly being filtered down
        for item_detector in self.item_detectors:
            (
                filtered_stashes,
                item_count,
                n_unique_found_items,
                leftover_stashes,
            ) = item_detector.iterate_stashes(stashes)

            wanted_stashes += filtered_stashes
            n_new_items += item_count
            n_total_unique_items += n_unique_found_items

            stashes = leftover_stashes

        # Updates progress bars
        self.n_found_items += n_new_items
        self.item_count_pbar.update(n_new_items)

        self.unique_items_count_pbar.update(
            n_total_unique_items
            - self.n_unique_items_found  # Updates with the difference of current unique items found and previously found
        )
        self.n_unique_items_found = n_total_unique_items

        return wanted_stashes

    def _initialize_stream(self, next_change_id) -> tuple:
        """
        TODO
        """
        response = requests.get(
            self.url, headers=self.headers, params={"id": next_change_id}
        )
        if response.status_code >= 300:
            response.raise_for_status()
        response_json = response.json()

        stashes = response_json["stashes"]
        next_change_id = response_json["next_change_id"]

        self.iteration_pbar.update()
        return next_change_id, stashes

    async def _start_next_request(self, session, next_change_id: str) -> Coroutine:
        async with session.get(self.url, params={"id": next_change_id}) as response:
            if response.status >= 300:
                if response.status == 429:
                    # https://www.pathofexile.com/developer/docs/index#ratelimits
                    # Rate limits are dynamic
                    headers = await response.headers
                    retry_after = int(headers["Retry-After"])
                    await asyncio.sleep(retry_after + 1)
                else:
                    response.raise_for_status()
            response_json = await response.json()
            next_change_id = response_json["next_change_id"]
            stashes = response_json["stashes"]
            return next_change_id, stashes

    async def _follow_stream(self, initial_next_change_id) -> None:
        """
        Follows the API stream until conditions are met

        Parameters:
            :param initial_next_change_id: (str) A previously found `next_change_id`.
            :param first_stashes: (list) A list of stash objects which have already been found.
        """
        next_change_id, new_stashes = self._initialize_stream(initial_next_change_id)
        stashes = []

        iteration = 2
        session = aiohttp.ClientSession(headers=self.headers)
        try:
            # async with aiohttp.ClientSession(headers=self.headers) as session:
            while (
                self.n_found_items < self.n_wanted_items
                or self.n_unique_items_found < self.n_unique_wanted_items
            ):
                future = asyncio.ensure_future(
                    self._start_next_request(session, next_change_id=next_change_id)
                )

                wanted_stashes = self._check_stashes(stashes=new_stashes)
                stashes += wanted_stashes

                self.iteration_pbar.update()

                task_response = await asyncio.gather(future)
                next_change_id, new_stashes = task_response[0]

                # if iteration >= max_iterations:
                #     break
                if not new_stashes:
                    time.sleep(
                        300
                    )  # Waits 5 minutes before continuing to persue the stream

                iteration += 1
        except requests.HTTPError as e:
            print(e)
        finally:  # Probably needs some more exception catches
            await session.close()
            self.iteration_pbar.close()
            self.item_count_pbar.close()
            self.unique_items_count_pbar.close()
            print(f"Final `next_change_id`: {next_change_id}")
            # self._store_data(stashes=stashes)

    async def dump_stream(
        self, initial_next_change_id: str = None, max_iterations: int = None
    ) -> None:
        """
        The method which begins making API calls and fetching data.

        Parameters:
            :param initial_next_change_id: (str) A previously found `next_change_id`.
            :param max_iterations: (int) The number of iteration before shutting down. (currently not implemented)
        """

        # Intializes progressbar context managers
        with (
            tqdm(
                total=max_iterations, desc="Iterations", position=0
            ) as self.iteration_pbar,
            tqdm(
                total=self.n_wanted_items,
                desc="    Items found",
                unit="item",
                position=1,
            ) as self.item_count_pbar,
            tqdm(
                total=self.n_unique_wanted_items,
                desc="    Unique items found",
                unit="item",
                position=2,
            ) as self.unique_items_count_pbar,
        ):
            try:
                await self._follow_stream(initial_next_change_id)
            except KeyboardInterrupt:
                print("Exiting program")
