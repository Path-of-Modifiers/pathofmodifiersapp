import numpy as np
import asyncio
from datetime import datetime
import threading
import time
from collections.abc import Iterator
from concurrent.futures import FIRST_EXCEPTION, ThreadPoolExecutor, wait

import aiohttp
import pandas as pd

from data_retrieval_app.utils import insert_data
from data_retrieval_app.tests.scripts.create_public_stashes_test_data.config import (
    script_settings,
)
from data_retrieval_app.external_data_retrieval.data_retrieval.poe_api_handler import (
    PoEAPIHandler,
)
from data_retrieval_app.external_data_retrieval.data_retrieval.poe_ninja_currency_api_handler import (
    PoENinjaCurrencyAPIHandler,
)
from data_retrieval_app.external_data_retrieval.main import ContinuousDataRetrieval
from data_retrieval_app.external_data_retrieval.transforming_data.transform_poe_api_data import (
    PoEAPIDataTransformerBase,
)
from data_retrieval_app.external_data_retrieval.transforming_data.transform_poe_ninja_currency_api_data import (
    TransformPoENinjaCurrencyAPIData,
)
from data_retrieval_app.external_data_retrieval.utils import (
    ProgramRunTooLongException,
    ProgramTooSlowException,
    sync_timing_tracker,
)
from data_retrieval_app.tests.scripts.create_public_stashes_test_data.main import (
    iterate_create_public_stashes_test_data,
)
from data_retrieval_app.logs.logger import test_logger, setup_logging


class TestPoEAPIDataTransformerBase(PoEAPIDataTransformerBase):
    def _add_timing_item_modifier_table(self, df: pd.DataFrame) -> pd.DataFrame:
        """Implemented in test child functions"""
        raise NotImplementedError("Only available in child classes")

    def _process_item_modifier_table(
        self, df: pd.DataFrame, item_id: pd.Series
    ) -> None:
        item_modifier_df = self._create_item_modifier_table(df, item_id=item_id)
        item_modifier_df = self._transform_item_modifier_table(item_modifier_df)
        item_modifier_df = self._add_timing_item_modifier_table(item_modifier_df)
        item_modifier_df = self._clean_item_modifier_table(item_modifier_df)

        insert_data(
            item_modifier_df,
            url=self.url,
            logger=test_logger,
            table_name="itemModifier",
            headers=self.pom_auth_headers,
        )


class TestUniquePoEAPIDataTransformer(TestPoEAPIDataTransformerBase):
    def _add_timing_item_modifier_table(self, df: pd.DataFrame) -> pd.DataFrame:
        if not script_settings.dispersed_timing_enabled:
            return df
        dati = script_settings.DAYS_AMOUNT_TIMING_INTERVAL
        test_logger.info(f"Amount of days creating timing interval for: {dati}")
        df_size = df.size
        df_chunks = [df.copy()]
        if df_size == max(df_size, dati):
            test_logger.info(f"Df size adding timing: {df_size}")
            df_chunks = np.array_split(df, dati)

        for day, chunk in enumerate(df_chunks):
            month = day // 30
            year = month // 12

            chunk["createdAt"] = datetime(2020 + year, month + 1, day + 1).isoformat()
        df_combined: pd.DataFrame = pd.concat(df_chunks, ignore_index=True)  # type: ignore

        return df_combined

    def _transform_item_modifier_table(
        self, item_modifier_df: pd.DataFrame
    ) -> pd.DataFrame:
        item_modifier_df = self.roll_processor.add_rolls(df=item_modifier_df)

        return item_modifier_df

    def _clean_item_modifier_table(self, item_modifer_df: pd.DataFrame) -> pd.DataFrame:
        """
        Gets rid of unnecessay information, so that only fields needed for the DB remains.
        """
        item_modifer_df.drop(
            item_modifer_df.columns.difference(
                ["itemId", "modifierId", "orderId", "position", "roll", "createdAt"]
            ),
            axis=1,
            inplace=True,
        )
        return item_modifer_df

    def _create_item_modifier_table(
        self, df: pd.DataFrame, *, item_id: pd.Series
    ) -> pd.DataFrame:
        """
        A similiar process to creating the item table, only this time the
        relevant column contains a list and not a JSON-object
        """
        self.item_modifier_columns = ["name", "explicitMods"]

        item_modifier_df = df.loc[:, self.item_modifier_columns].reset_index()

        item_modifier_df["itemId"] = item_id
        item_modifier_df = item_modifier_df.explode("explicitMods", ignore_index=True)

        item_modifier_df.rename({"explicitMods": "modifier"}, axis=1, inplace=True)

        return item_modifier_df


class TestModifierSimulatedDataPoEAPIHandler(PoEAPIHandler):
    async def _follow_stream(
        self,
        stashes_ready_event: threading.Event,
        waiting_for_next_id_lock: threading.Lock,
        stash_lock: threading.Lock,
    ) -> None:
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
        except Exception as e:
            test_logger.info(
                f"The following exception occured during {self._follow_stream}: {e} {e.args}"
            )
            raise e
        finally:

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

        stashes_local = self.stashes
        del self.stashes
        self.stashes = []

        self.requests_since_last_checkpoint = 0
        stash_lock.release()
        stashes_ready_event.clear()

        wandted_df = self._check_stashes(stashes_local)
        df = pd.concat((df, wandted_df))
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
                df = self._gather_n_checkpoints(stashes_ready_event, stash_lock, n=1)
                test_logger.info(
                    "Finished processing the stream, entering transformation phase"
                )
                yield df.reset_index()
                del df
                raise ProgramRunTooLongException  # Script exits here


class TestModifierSimulatedDataContinuousDataRetrieval(ContinuousDataRetrieval):
    def __init__(
        self,
        items_per_batch: int,
        data_transformers: dict[str, PoEAPIDataTransformerBase],
    ):
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

    def retrieve_data(self) -> None:
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


def main() -> None:
    """
    Tests backend data retrieval with deposit data simulated with mocked
    PoE API docs objects.
    """
    setup_logging()
    items_per_batch = 1
    data_transformers = {"unique": TestUniquePoEAPIDataTransformer}
    data_retriever = TestModifierSimulatedDataContinuousDataRetrieval(
        items_per_batch=items_per_batch, data_transformers=data_transformers
    )
    data_retriever.retrieve_data()


if __name__ == "__main__":
    main()
