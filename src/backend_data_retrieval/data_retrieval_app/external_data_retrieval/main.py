from concurrent.futures import (
    ALL_COMPLETED,
    FIRST_COMPLETED,
    Future,
    ThreadPoolExecutor,
    wait,
)
from io import StringIO
from typing import Any

import pandas as pd

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.external_data_retrieval.data_retrieval.currency_api_handler import (
    CurrencyAPIHandler,
)
from data_retrieval_app.external_data_retrieval.data_retrieval.poe_api_handler import (
    PoEAPIHandler,
)
from data_retrieval_app.external_data_retrieval.transforming_data.transform_currency_api_data import (
    TransformCurrencyAPIData,
)
from data_retrieval_app.external_data_retrieval.transforming_data.transform_poe_api_data import (
    PoEAPIDataTransformerBase,
    UniquePoEAPIDataTransformer,
)
from data_retrieval_app.external_data_retrieval.utils import (
    ProgramFinished,
    ProgramTooSlowException,
)
from data_retrieval_app.logs.logger import external_data_retrieval_logger as logger
from data_retrieval_app.logs.logger import setup_logging
from data_retrieval_app.pom_api_authentication import (
    get_superuser_token_headers,
)
from data_retrieval_app.utils import find_hours_since_launch, get_data_safe


class ContinuousDataRetrieval:
    auth_token = settings.POE_PUBLIC_STASHES_AUTH_TOKEN
    stash_tab_url = "https://api.pathofexile.com/public-stash-tabs"

    backend_base_url = settings.BACKEND_BASE_URL
    modifier_url = f"{backend_base_url}/modifier/"
    active_league_url = f"{backend_base_url}/league/active_league/"
    item_base_type_url = f"{backend_base_url}/itemBaseType/"
    currency_url = f"{backend_base_url}/currency/"
    pom_auth_headers = get_superuser_token_headers(backend_base_url)

    def __init__(
        self,
        items_per_batch: int,
        data_transformers: dict[str, PoEAPIDataTransformerBase],
    ):
        self.leagues = self._get_leagues()
        self.data_transformers: dict[str, PoEAPIDataTransformerBase] = {
            key: data_transformer(self.leagues)
            for key, data_transformer in data_transformers.items()
        }

        self.poe_api_handler = PoEAPIHandler(
            url=self.stash_tab_url,
            auth_token=self.auth_token,
            leagues=self.leagues,
            n_wanted_items=items_per_batch,
            n_unique_wanted_items=10,
        )

        self.currency_api_handler = CurrencyAPIHandler(
            url="https://api.poe.watch/exchange/ratios?league={league}&game=poe1"
        )
        self.currency_transformer = TransformCurrencyAPIData()

    def _get_modifiers(self) -> dict[str, pd.DataFrame]:
        response = get_data_safe(
            self.modifier_url, headers=self.pom_auth_headers, logger=logger
        )
        # Check if the request was successful
        modifier_df = pd.DataFrame()
        # Load the JSON data into a pandas DataFrame
        json_io = StringIO(response.content.decode("utf-8"))
        modifier_df = pd.read_json(json_io, dtype=str)

        modifier_types = [
            "implicit",
            "explicit",
            "delve",
            "fractured",
            "synthesised",
            "unique",
            "corrupted",
            "enchanted",
            "veiled",
        ]
        modifier_dfs = {}
        for modifier_type in modifier_types:
            if modifier_type in modifier_df.columns:
                modifier_dfs[modifier_type] = modifier_df.loc[
                    ~modifier_df[modifier_type].isna()
                ]
        return modifier_dfs

    def _get_leagues(self) -> list[dict[str, Any]]:
        response = get_data_safe(
            self.active_league_url, headers=self.pom_auth_headers, logger=logger
        )
        leagues = response.json()

        return leagues

    def _get_item_base_types(self) -> dict[str, int]:
        response = get_data_safe(
            self.item_base_type_url, headers=self.pom_auth_headers, logger=logger
        )
        item_base_type_mapped = {}
        item_base_types = []

        item_base_types = response.json()
        if not isinstance(item_base_types, list):
            item_base_types = [item_base_types]
        for item_base_type in item_base_types:
            item_base_type_id = item_base_type["itemBaseTypeId"]
            base_type = item_base_type["baseType"]
            item_base_type_mapped[base_type] = item_base_type_id

        return item_base_type_mapped

    def _categorize_new_items(self, df: pd.DataFrame) -> dict[str, pd.DataFrame]:
        split_dfs = {}

        # TODO not fully exhaustive yet, needs to be updated over time
        # category_priority = [
        # "synthesised",
        # "fractured",
        # "delve",
        # "veiled",
        # "unique",
        # ]
        # Needs to take priority, see nebulis and rational doctrine
        # not_synth_mask = df["synthesised"].isna()
        # split_dfs["synthesised"] = df.loc[~not_synth_mask]
        # df = df.loc[not_synth_mask]

        not_unique_mask = df["rarity"] != "Unique"
        split_dfs["unique"] = df.loc[~not_unique_mask]
        df = df.loc[not_unique_mask]

        # for category in category_priority:
        #     mask = df[category].isna()

        #     split_dfs[category] = df.loc[~mask]
        #     df = df.loc[mask]

        return split_dfs

    def _get_new_currency_data(self, current_hour: int) -> pd.DataFrame:
        response = get_data_safe(
            self.currency_url + "latest_hour/",
            headers=self.pom_auth_headers,
            logger=logger,
        )

        latest_hour = response.json()
        if latest_hour == current_hour:
            response = get_data_safe(
                self.currency_url + "latest_currencies/",
                headers=self.pom_auth_headers,
                logger=logger,
            )

            currency_df = pd.DataFrame(response.json())
        else:
            currency_df = self.currency_api_handler.make_request(self.leagues)
            currency_df = self.currency_transformer.transform_into_tables(
                currency_df, current_hour
            )

        return currency_df

    def _initialize_data_stream_threads(
        self, executor: ThreadPoolExecutor, listeners: int, has_crashed: bool = False
    ) -> dict[Future, str]:
        return self.poe_api_handler.initialize_data_stream_threads(
            executor, listeners, has_crashed
        )

    def _follow_data_dump_stream(self):
        try:
            current_hours = find_hours_since_launch(self.leagues)
            # Only need to refer to one league to see when a new hour starts
            current_hour = current_hours[self.leagues[0]["leagueId"]]
            next_hour = current_hour + 1
            logger.info("Retrieving modifiers from db.")
            modifier_dfs = self._get_modifiers()
            item_base_types = self._get_item_base_types()
            currency_df = self._get_new_currency_data(current_hour)
            get_df = self.poe_api_handler.dump_stream()
            while current_hour < next_hour:
                df = next(get_df)
                split_dfs = self._categorize_new_items(df)
                for data_transformer_type in self.data_transformers:
                    self.data_transformers[data_transformer_type].transform_into_tables(
                        df=split_dfs[data_transformer_type],
                        modifier_df=modifier_dfs[data_transformer_type],
                        currency_df=currency_df.copy(deep=True),
                        item_base_types=item_base_types,
                        current_hours=current_hours,
                    )
                current_hours = find_hours_since_launch(self.leagues)
                current_hour = current_hours[self.leagues[0]["leagueId"]]
            for data_transformer_type in self.data_transformers:
                self.data_transformers[data_transformer_type].end_of_hour_cleanup()

            raise ProgramFinished

        except ProgramFinished:
            raise
        except ProgramTooSlowException:
            raise
        except Exception as e:
            logger.exception(
                f"The following exception occured during '_follow_data_dump_stream': {e}"
            )
            raise

    def retrieve_data(self):
        logger.info("Program starting up.")
        logger.info("Initiating data stream.")
        max_workers = 3
        listeners = max(
            max_workers - 1, 1
        )  # minus one because of transformation threads
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = self._initialize_data_stream_threads(
                executor, listeners=listeners
            )
            follow_future = executor.submit(self._follow_data_dump_stream)
            futures[follow_future] = "data_processing"
            logger.info("Waiting for futures to crash.")
            finished = False
            while True:
                if finished:
                    return
                done_futures, _ = wait(futures, return_when=FIRST_COMPLETED)
                while done_futures:
                    future = done_futures.pop()
                    future_job = futures.pop(future)

                    if future_job == "data_processing":
                        try:
                            future.result()
                        except ProgramTooSlowException:
                            logger.info(
                                f"The job '{future_job}' was too slow. Restarting..."
                            )
                            self.poe_api_handler.set_program_too_slow()

                            wait(futures, return_when=ALL_COMPLETED)

                            finished = True
                        except ProgramFinished:
                            logger.info(
                                f"The job '{future_job}' has finished this cycle. Restarting..."
                            )
                            self.poe_api_handler.set_program_finished()

                            wait(futures, return_when=ALL_COMPLETED)
                            finished = True
                        except Exception:
                            logger.exception(
                                f"The following exception occured in job '{future_job}': {future.exception()}"
                            )
                            follow_future = executor.submit(
                                self._follow_data_dump_stream
                            )
                            futures[follow_future] = "data_processing"
                    elif future_job == "listener":
                        new_future = self._initialize_data_stream_threads(
                            executor,
                            listeners=1,
                            has_crashed=True,
                        )
                        futures[new_future] = "listener"


def main():
    logger.info("Starting the program...")
    setup_logging()
    items_per_batch = 300
    data_transformers = {"unique": UniquePoEAPIDataTransformer}

    data_retriever = ContinuousDataRetrieval(
        items_per_batch=items_per_batch,
        data_transformers=data_transformers,
    )
    data_retriever.retrieve_data()


if __name__ == "__main__":
    main()
