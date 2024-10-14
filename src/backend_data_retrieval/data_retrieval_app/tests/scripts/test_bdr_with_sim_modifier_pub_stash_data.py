import asyncio
import copy
import threading
import time
from collections.abc import Iterator
from concurrent.futures import ALL_COMPLETED, FIRST_EXCEPTION, ThreadPoolExecutor, wait

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
from data_retrieval_app.tests.scripts.create_public_stashes_test_data.utils.modifier_test_data_creator import (
    DataDepositTestDataCreator,
)
from data_retrieval_app.tests.scripts.create_public_stashes_test_data.utils.scrap_and_mock_poe_api_docs_objs import (
    ScrapAndMockPoEAPIDocsObjs,
)
from data_retrieval_app.tests.utils import replace_false_values


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
            self.stashes += stashes
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
        scrap_and_mock_poe_api_docs_objs = ScrapAndMockPoEAPIDocsObjs()
        (
            public_stashes_mock_obj,
            item_mock_obj,
        ) = scrap_and_mock_poe_api_docs_objs.produce_mocks_from_docs()
        public_stashes_modifier_test_data_creator = DataDepositTestDataCreator(
            n_of_items=1000
        )

        all_stashes = []
        for (
            file_name,
            items,
        ) in public_stashes_modifier_test_data_creator.create_test_data_with_data_deposit_files():
            test_logger.info(f"Processing items from file '{file_name}'")
            current_public_stashes_mock_modified = replace_false_values(
                copy.deepcopy(public_stashes_mock_obj)
            )
            for item in items:
                merged_complete_item_dict = {**item_mock_obj, **item}
                merged_complete_item_dict_modified = replace_false_values(
                    copy.deepcopy(merged_complete_item_dict)
                )
                current_public_stashes_mock_modified["items"].append(
                    merged_complete_item_dict_modified
                )

            all_stashes.append(current_public_stashes_mock_modified)

        stashes_local = all_stashes
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
            start_time = time.perf_counter()
            df = self._process_stream(stashes_ready_event, stash_lock, df)
            end_time = time.perf_counter()

            time_per_mini_batch = end_time - start_time
            if time_per_mini_batch > (2 * 60):
                # Does not allow a batch to take longer than 2 minutes
                raise ProgramTooSlowException

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
                df = self._gather_n_checkpoints(stashes_ready_event, stash_lock)
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
                test_logger.info("Waiting for futures to crash.")
                done_futures, not_done_futures = wait(
                    futures, return_when=FIRST_EXCEPTION
                )
                crashed_future = list(done_futures)[0]
                future_job = futures.pop(crashed_future)
                test_logger.info(
                    f"The future '{future_job}' has crashed. Finding exception..."
                )
                if future_job == "data_processing":
                    crashed_future_exception = crashed_future.exception()
                    try:
                        raise crashed_future_exception
                    except ProgramTooSlowException:
                        test_logger.info(
                            f"The job '{future_job}' was too slow. Restarting..."
                        )
                        self.poe_api_handler.set_program_too_slow()

                        wait(futures, return_when=ALL_COMPLETED)

                        raise ProgramTooSlowException
                    except ProgramRunTooLongException:
                        test_logger.info(
                            f"The job '{future_job}' has been running too long. Restarting..."
                        )
                        self.poe_api_handler.set_program_too_slow()

                        wait(futures, return_when=ALL_COMPLETED)
                        raise ProgramRunTooLongException
                    except Exception:
                        test_logger.exception(
                            f"The following exception occured in job '{future_job}': {crashed_future_exception}"
                        )
                        follow_future = executor.submit(self._follow_data_dump_stream)
                        futures[follow_future] = "data_processing"
                elif future_job == "listener":
                    new_future = self._initialize_data_stream_threads(
                        executor,
                        listeners=1,
                        has_crashed=True,
                    )
                    futures[new_future] = "listener"
        except ProgramTooSlowException:
            test_logger.info("Program was too slow. Restarting...")
        except ProgramRunTooLongException:
            test_logger.info("Program has run too long. Restarting...")
        except Exception as e:
            test_logger.exception(f"The following exception occured: {e}")
            raise e


def main():
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
