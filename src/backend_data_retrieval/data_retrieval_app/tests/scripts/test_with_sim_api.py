import threading
from typing import Any

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
    def __init__(self, leagues: dict[str, Any]):
        super().__init__(leagues)

    def _create_random_time_column(self, length: int) -> pd.Series:
        random_times = np.random.randint(0, script_settings.TIMING_PERIOD * 24, length)

        return pd.Series(random_times, dtype=int)

    def _transform_item_table(
        self,
        item_df: pd.DataFrame,
        currency_df: pd.DataFrame,
        item_base_types: dict[str, int],
        current_hours: dict[int, int],
    ) -> pd.DataFrame:
        item_df = super()._transform_item_table(
            item_df, currency_df, item_base_types, current_hours
        )
        if script_settings.dispersed_timing_enabled:
            item_df["createdHoursSinceLaunch"] += self.time_column

        return item_df

    def _create_item_modifier_table(
        self,
        df: pd.DataFrame,
        *,
        item_id: pd.Series,
        current_hours: dict[int, int],
    ) -> pd.DataFrame:
        """
        A similiar process to creating the item table, only this time the
        relevant column contains a list and not a JSON-object
        """
        # This method does the exact same thing, except adding random time if enabled
        # This needs to be done before explode, but after filtering extremly priced items
        item_modifier_columns = ["name", "explicitMods", "league"]
        item_modifier_df = df.loc[
            self.price_found_mask,
            item_modifier_columns,
        ]

        item_modifier_df = item_modifier_df.loc[
            self.items_not_too_high_priced_mask
        ].reset_index()

        item_modifier_df["itemId"] = item_id
        item_modifier_df["leagueId"] = item_modifier_df["league"].map(self.league_to_id)
        item_modifier_df["createdHoursSinceLaunch"] = item_modifier_df["leagueId"].map(
            current_hours
        )
        if script_settings.dispersed_timing_enabled:
            item_modifier_df["createdHoursSinceLaunch"] += self.time_column
        item_modifier_df = item_modifier_df.explode("explicitMods", ignore_index=True)

        item_modifier_df.rename({"explicitMods": "modifier"}, axis=1, inplace=True)

        return item_modifier_df

    def transform_into_tables(
        self,
        df: pd.DataFrame,
        modifier_df: pd.DataFrame,
        currency_df: pd.DataFrame,
        item_base_types: dict[str, int],
        current_hours: dict[int, int],
    ) -> None:
        if script_settings.dispersed_timing_enabled:
            self.time_column = self._create_random_time_column(length=len(df))

        test_logger.info(
            f"Transforming {len(df)} items, making them ready to insert into db"
        )
        super().transform_into_tables(
            df, modifier_df, currency_df, item_base_types, current_hours
        )


class PoEMockAPIHandler(PoEAPIHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.mock_api = PublicStashMockAPI(leagues=kwargs["leagues"])

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
            url=self.stash_tab_url,
            auth_token=self.auth_token,
            leagues=self.leagues,
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
