import numpy as np
import asyncio
from datetime import datetime
import threading
import time
from typing import Iterator
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

    def _add_timing_item_table(
        self, split_item_dfs_by_unique_names: list[pd.DataFrame]
    ) -> pd.DataFrame:
        if not script_settings.dispersed_timing_enabled:
            return pd.concat(split_item_dfs_by_unique_names, ignore_index=True)
        dati = script_settings.DAYS_AMOUNT_TIMING_INTERVAL

        item_dfs_combined = []
        test_logger.info("Adding timing to the item tables")
        for item_df in split_item_dfs_by_unique_names:
            df_size = item_df.size
            df_chunks = [item_df.copy()]
            if df_size == max(df_size, dati):
                df_chunks = np.array_split(item_df, dati)

            for day, chunk in enumerate(df_chunks):
                month = day // 30
                year = month // 12

                chunk["createdAt"] = datetime(
                    2020 + year, month + 1, day + 1
                ).isoformat()
            item_named_df_combined: pd.DataFrame = pd.concat(df_chunks, ignore_index=True)  # type: ignore
            item_dfs_combined.append(item_named_df_combined)
        item_df_combined: pd.DataFrame = pd.concat(item_dfs_combined, ignore_index=True)
        return item_df_combined

    def _split_item_table_by_item_name(
        self, item_df: pd.DataFrame
    ) -> list[pd.DataFrame]:
        unique_item_names = item_df["name"].unique()

        split_by_unique_item_names_dfs = []
        for unique_name in unique_item_names:
            unique_item_name_mask_df = item_df["name"] == unique_name
            split_by_unique_item_names_dfs.append(item_df[unique_item_name_mask_df])

        return split_by_unique_item_names_dfs

    def _transform_item_table(
        self, item_df: pd.DataFrame, currency_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        The `item` table requires a foreign key to the `currency` table.
        Everything related to the price of the item is stored in the `node`
        attribute.

        There are two types of listings in PoE, exact price and asking price which are
        represented by `price` and `b/o` respectively.
        """

        def get_currency_amount(element):
            if isinstance(element, list):
                if len(element) == 3:
                    return element[1] if element[0] in ["~b/o", "~price"] else pd.NA

            return pd.NA

        def get_currency_type(element):
            if isinstance(element, list):
                if len(element) == 3:
                    return element[2] if element[0] in ["~b/o", "~price"] else ""

            return ""

        def transform_influences(row: pd.DataFrame, influence_columns: list[str]):
            if not row[influence_columns].any():
                return pd.NA
            else:
                influence_dict = {}
                for influence_column in influence_columns:
                    if row[influence_column]:
                        influence_dict[influence_column.replace("influences.", "")] = (
                            True
                        )
                return influence_dict

        influence_columns = [
            column for column in item_df.columns if "influences" in column
        ]
        item_df["influences"] = item_df.apply(
            lambda row: transform_influences(row, influence_columns), axis=1
        )

        stash_series = item_df["stash"].str.split(" ")
        currency_series = item_df["note"].str.split(" ")

        currency_series = currency_series.where(
            item_df["note"].str.contains("~"), stash_series
        )
        item_df["currencyAmount"] = currency_series.apply(get_currency_amount)
        item_df["currencyType"] = currency_series.apply(get_currency_type)

        invalid_amount_mask = ~item_df["currencyAmount"].str.match(
            r"^(([0-9]*[.])?[0-9]+)$", na=False
        )
        item_df.loc[invalid_amount_mask, "currencyAmount"] = pd.NA
        item_df.loc[invalid_amount_mask, "currencyType"] = ""

        item_df = item_df.merge(
            currency_df, how="left", left_on="currencyType", right_on="tradeName"
        )

        return item_df

    def _process_item_table(
        self, df: pd.DataFrame, currency_df: pd.DataFrame
    ) -> pd.Series:
        test_logger.info("Processing item tables...")
        test_logger.info(f"Total items to process: {df.size}")
        item_df = self._create_item_table(df)
        item_df = self._transform_item_table(item_df, currency_df)
        split_by_unique_name_item_df = self._split_item_table_by_item_name(item_df)
        item_df = self._add_timing_item_table(split_by_unique_name_item_df)
        item_df = self._clean_item_table(item_df)
        test_logger.info("Finished preprocessing the item tables")

        test_logger.info("Posting items the pom API...")
        insert_data(
            item_df,
            url=self.url,
            table_name="item",
            logger=test_logger,
            headers=self.pom_auth_headers,
        )
        test_logger.info("Finished posting the items to pom API")

        test_logger.info("Finding latest item id...")
        item_id = self._get_latest_item_id_series(item_df)
        test_logger.debug("Latest item id found: " + str(item_id))
        return item_id

    def _clean_item_table(self, item_df: pd.DataFrame) -> pd.DataFrame:
        """
        Gets rid of unnecessay information, so that only fields needed for the DB remains.
        """
        drop_list = [
            "influences.shaper",
            "influences.elder",
            "influences.crusader",
            "influences.hunter",
            "influences.redeemer",
            "influences.warlord",
            "stash",
            "currencyType",
            "tradeName",
            "valueInChaos",
            "itemId",
            "iconUrl",
        ]
        item_df.drop(
            drop_list,
            axis=1,
            inplace=True,
            errors="ignore",
        )

        item_df.rename({"icon": "iconUrl"}, axis=1, inplace=True)
        return item_df

    def _process_item_modifier_table(
        self, df: pd.DataFrame, item_id: pd.Series
    ) -> None:
        test_logger.info("Processing item tables...")
        test_logger.info(f"Total item modifiers to process: {df.size}")
        item_modifier_df = self._create_item_modifier_table(df, item_id=item_id)
        item_modifier_df = self._transform_item_modifier_table(item_modifier_df)
        item_modifier_df = self._clean_item_modifier_table(item_modifier_df)
        test_logger.info("Finished preprocessing the item tables")

        test_logger.info("Posting items the pom API...")
        insert_data(
            item_modifier_df,
            url=self.url,
            table_name="itemModifier",
            logger=test_logger,
            headers=self.pom_auth_headers,
        )
        test_logger.info("Finished posting the items to pom API")


class TestUniquePoEAPIDataTransformer(TestPoEAPIDataTransformerBase):
    """Nothing changed in this class, it just needs to inherit and override functions properly"""

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
                ["itemId", "modifierId", "orderId", "position", "roll"]
            ),
            axis=1,
            inplace=True,
        )

        return item_modifer_df


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
