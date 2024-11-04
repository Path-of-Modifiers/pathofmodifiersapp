import threading

import numpy as np
import pandas as pd

from data_retrieval_app.external_data_retrieval.data_retrieval.poe_api_handler import (
    PoEAPIHandler,
)
from data_retrieval_app.external_data_retrieval.main import ContinuousDataRetrieval
from data_retrieval_app.external_data_retrieval.transforming_data.transform_poe_api_data import (
    PoEAPIDataTransformerBase,
    UniquePoEAPIDataTransformer,
)
from data_retrieval_app.logs.logger import setup_logging, test_logger
from data_retrieval_app.tests.scripts.create_public_stashes_test_data.config import (
    script_settings,
)
from data_retrieval_app.tests.scripts.create_public_stashes_test_data.main import (
    PublicStashMockAPI,
)


class TestUniquePoEAPIDataTransformer(UniquePoEAPIDataTransformer):
    def __init__(self):
        super().__init__()

        self._update_item_table_columns_to_drop(dont_drop={"createdAt"})
        self._update_item_modifier_table_columns_to_not_drop(dont_drop={"createdAt"})

    def _create_random_time_column(self, length: int) -> pd.Series:
        start = pd.to_datetime("1990-01-01")

        timedelta_series = pd.to_timedelta(
            np.random.randint(0, script_settings.TIMING_PERIOD, length), unit="D"
        )

        time_column = timedelta_series + start

        return time_column.astype(str)

    def _create_item_table(self, df):
        item_df = super()._create_item_table(df)
        if script_settings.dispersed_timing_enabled:
            item_df["createdAt"] = self.time_column

        return item_df

    def _create_item_modifier_table(
        self, df: pd.DataFrame, *, item_id: pd.Series
    ) -> pd.DataFrame:
        """
        A similiar process to creating the item table, only this time the
        relevant column contains a list and not a JSON-object
        """
        item_modifier_columns = ["name", "explicitMods"]

        if script_settings.dispersed_timing_enabled:
            df["createdAt"] = self.time_column
            item_modifier_columns.append("createdAt")

        item_modifier_df = df.loc[:, item_modifier_columns].reset_index()

        item_modifier_df["itemId"] = item_id
        item_modifier_df = item_modifier_df.explode("explicitMods", ignore_index=True)

        item_modifier_df.rename({"explicitMods": "modifier"}, axis=1, inplace=True)

        return item_modifier_df

    def transform_into_tables(
        self,
        df: pd.DataFrame,
        modifier_df: pd.DataFrame,
        currency_df: pd.DataFrame,
    ) -> None:
        if script_settings.dispersed_timing_enabled:
            self.time_column = self._create_random_time_column(length=len(df))

        super().transform_into_tables(df, modifier_df, currency_df)


class PoEMockAPIHandler(PoEAPIHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.mock_api = PublicStashMockAPI()
        self.run_program_for_n_seconds = script_settings.CREATE_TEST_DATA_FOR_N_SECONDS
        self.n_checkpoints_per_transfromation = (
            script_settings.N_CHECKPOINTS_PER_TRANSFORMATION
        )

    async def _follow_stream(
        self,
        stashes_ready_event: threading.Event,
        waiting_for_next_id_lock: threading.Lock,  # noqa: ARG002
        stash_lock: threading.Lock,
    ) -> None:
        mini_batch_size = script_settings.MINI_BATCH_SIZE
        while True:
            while self.requests_since_last_checkpoint < mini_batch_size:
                stashes = self.mock_api.get_test_data()

                stash_lock.acquire()
                self.stashes += stashes
                self.requests_since_last_checkpoint += 1
                stash_lock.release()

            stashes_ready_event.set()


class ContinuousMockDataRetrieval(ContinuousDataRetrieval):
    def __init__(
        self,
        items_per_batch: int,
        data_transformers: dict[str, PoEAPIDataTransformerBase],
    ):
        super().__init__(items_per_batch, data_transformers)

        self.poe_api_handler = PoEMockAPIHandler(
            url=self.url,
            auth_token=self.auth_token,
            n_wanted_items=items_per_batch,
            n_unique_wanted_items=10,
        )


def main():
    test_logger.info("Starting the program...")
    setup_logging()
    items_per_batch = 300
    data_transformers = {"unique": TestUniquePoEAPIDataTransformer}

    data_retriever = ContinuousMockDataRetrieval(
        items_per_batch=items_per_batch,
        data_transformers=data_transformers,
    )
    data_retriever.retrieve_data()


if __name__ == "__main__":
    main()
