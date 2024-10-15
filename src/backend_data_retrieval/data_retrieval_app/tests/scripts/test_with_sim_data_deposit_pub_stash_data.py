import asyncio
import threading
import time
from collections.abc import Iterator
from concurrent.futures import FIRST_EXCEPTION, ThreadPoolExecutor, wait

import aiohttp
import pandas as pd

from data_retrieval_app.external_data_retrieval.data_retrieval.poe_api_handler import (
    PoEAPIHandler,
)
from data_retrieval_app.external_data_retrieval.data_retrieval.poe_ninja_currency_api_handler import (
    PoENinjaCurrencyAPIHandler,
)
from data_retrieval_app.external_data_retrieval.main import ContinuousDataRetrieval
from data_retrieval_app.external_data_retrieval.transforming_data.transform_poe_api_data import (
    PoEAPIDataTransformerBase,
    UniquePoEAPIDataTransformer,
)
from data_retrieval_app.external_data_retrieval.transforming_data.transform_poe_ninja_currency_api_data import (
    TransformPoENinjaCurrencyAPIData,
)
from data_retrieval_app.external_data_retrieval.utils import (
    ProgramRunTooLongException,
    ProgramTooSlowException,
    sync_timing_tracker,
)
from data_retrieval_app.logs.logger import setup_logging, test_logger
from data_retrieval_app.tests.scripts.create_public_stashes_test_data.main import (
    iterate_create_public_stashes_test_data,
)


class TestModifierSimulatedDataPoEAPIHandler(PoEAPIHandler):
    async def _follow_stream(
        self,
        stashes_ready_event: threading.Event,
        waiting_for_next_id_lock: threading.Lock,
        stash_lock: threading.Lock,
    ):
        """Overrides the function in PoEAPIHandler"""
        stashes = []  # For exeption handling

        timeout = aiohttp.ClientTimeout(total=60)
        session = aiohttp.ClientSession(headers=self.headers, timeout=timeout)
        try:
            stash_lock.acquire()
            all_stashes = []
            if not self.stashes:
                for _, _, stashes in iterate_create_public_stashes_test_data():
                    all_stashes.append(stashes[0])
                self.stashes += all_stashes
            stash_lock.release()
            del stashes

            stashes_ready_event.set()
            await asyncio.sleep(1)
        except:
            test_logger.exception(
                f"The following exception occured during {self._follow_stream}"
            )
            raise
        finally:
            test_logger.info(f"Exiting {self._follow_stream} gracefully")

            await session.close()

    @sync_timing_tracker
    def _process_stream(
        self,
        stashes_ready_event: threading.Event,
        stash_lock: threading.Lock,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Overrides the function in PoEAPIHandler"""

        stashes_ready_event.wait()
        stash_lock.acquire()

        test_logger.info("Stashes are ready for processing")

        stashes_local = self.stashes
        del self.stashes
        self.stashes = []

        self.requests_since_last_checkpoint = 0
        stash_lock.release()
        stashes_ready_event.clear()

        test_logger.debug("Copied stashes locally and reset the event")
        wandted_df = self._check_stashes(stashes_local)
        df = pd.concat((df, wandted_df))
        test_logger.info("Finished processing the data, waiting for more")
        return df

    def _gather_n_checkpoints(
        self,
        stashes_ready_event: threading.Event,
        stash_lock: threading.Lock,
        n: int = 1,
    ) -> pd.DataFrame:
        """Overrides the function in PoEAPIHandler"""
        df = pd.DataFrame()
        for _ in range(n):
            df = self._process_stream(stashes_ready_event, stash_lock, df)

        return df

    def dump_stream(self, track_progress: bool = True) -> Iterator[pd.DataFrame]:
        """Overrides the function in PoEAPIHandler"""
        try:
            stashes_ready_event = self.stashes_ready_event
            stash_lock = self.stash_lock
        except AttributeError:
            raise Exception("The method 'start_data_stream' must be called prior")
        else:
            time.sleep(5)  # Waits for the listening threads to have time to start up.
            while True:
                test_logger.info("Waiting for data from the stream")
                df = self._gather_n_checkpoints(stashes_ready_event, stash_lock, n=1)
                test_logger.info(
                    "Finished processing the stream, entering transformation phase"
                )
                yield df.reset_index()
                del df
                test_logger.info("Finished transformation phase")
                raise ProgramRunTooLongException  # Script exits here


class TestModifierSimulatedDataContinuousDataRetrieval(ContinuousDataRetrieval):
    def __init__(
        self,
        items_per_batch: int,
        data_transformers: dict[str, PoEAPIDataTransformerBase],
    ):
        """Overrides the function in ContinuousDataRetrieval"""
        self.data_transformers = {
            key: data_transformer()
            for key, data_transformer in data_transformers.items()
        }

        self.poe_api_handler = TestModifierSimulatedDataPoEAPIHandler(
            url=self.url,
            auth_token=self.auth_token,
            n_wanted_items=items_per_batch,
            n_unique_wanted_items=10,
        )

        self.poe_ninja_currency_api_handler = PoENinjaCurrencyAPIHandler(
            url=f"https://poe.ninja/api/data/currencyoverview?league={self.current_league}&type=Currency"
        )
        self.poe_ninja_transformer = TransformPoENinjaCurrencyAPIData()

    def retrieve_data(self):
        """Overrides the function in ContinuousDataRetrieval"""
        test_logger.info("Program starting up.")
        test_logger.info("Initiating data stream.")
        max_workers = 3
        listeners = max_workers - 1  # minus one because of transformation threa
        try:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = self._initialize_data_stream_threads(
                    executor, listeners=listeners
                )
                follow_future = executor.submit(self._follow_data_dump_stream)
                futures[follow_future] = "data_processing"
                done_futures, not_done_futures = wait(
                    futures, return_when=FIRST_EXCEPTION
                )
        except ProgramTooSlowException:
            test_logger.info("Program was too slow. Restarting...")
        except ProgramRunTooLongException:
            test_logger.info("Program has run too long. Restarting...")
        except Exception as e:
            test_logger.exception(f"The following exception occured: {e}")
            raise e


def main():
    """
    Tests backend data retrieval with deposit data simulated with mocked
    PoE API docs objects.
    """
    test_logger.info("Starting the program...")
    setup_logging()
    items_per_batch = 1
    data_transformers = {"unique": UniquePoEAPIDataTransformer}

    data_retriever = TestModifierSimulatedDataContinuousDataRetrieval(
        items_per_batch=items_per_batch,
        data_transformers=data_transformers,
    )
    data_retriever.retrieve_data()


if __name__ == "__main__":
    main()
