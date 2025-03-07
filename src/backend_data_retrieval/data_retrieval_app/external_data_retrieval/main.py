from concurrent.futures import (
    ALL_COMPLETED,
    FIRST_EXCEPTION,
    Future,
    ThreadPoolExecutor,
    wait,
)
from io import StringIO

import pandas as pd
import requests

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.external_data_retrieval.data_retrieval.poe_api_handler import (
    PoEAPIHandler,
)
from data_retrieval_app.external_data_retrieval.data_retrieval.poe_ninja_currency_api_handler import (
    PoENinjaCurrencyAPIHandler,
)
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
)
from data_retrieval_app.logs.logger import external_data_retrieval_logger as logger
from data_retrieval_app.logs.logger import setup_logging
from data_retrieval_app.pom_api_authentication import (
    get_superuser_token_headers,
)


class ContinuousDataRetrieval:
    auth_token = settings.POE_PUBLIC_STASHES_AUTH_TOKEN
    current_league = settings.CURRENT_SOFTCORE_LEAGUE
    url = "https://api.pathofexile.com/public-stash-tabs"

    if "localhost" not in settings.DOMAIN:
        base_pom_api_url = f"https://{settings.DOMAIN}/api/api_v1"
    else:
        base_pom_api_url = "http://src-backend-1/api/api_v1"
    modifier_url = base_pom_api_url + "/modifier/"
    item_base_type_url = base_pom_api_url + "/itemBaseType/"
    pom_auth_headers = get_superuser_token_headers(base_pom_api_url)

    def __init__(
        self,
        items_per_batch: int,
        data_transformers: dict[str, PoEAPIDataTransformerBase],
    ):
        self.data_transformers = {
            key: data_transformer()
            for key, data_transformer in data_transformers.items()
        }

        self.poe_api_handler = PoEAPIHandler(
            url=self.url,
            auth_token=self.auth_token,
            n_wanted_items=items_per_batch,
            n_unique_wanted_items=10,
        )

        self.poe_ninja_currency_api_handler = PoENinjaCurrencyAPIHandler(
            url=f"https://poe.ninja/api/data/currencyoverview?league={self.current_league}&type=Currency"
        )
        self.poe_ninja_transformer = TransformPoENinjaCurrencyAPIData()

    def _get_modifiers(self) -> dict[str, pd.DataFrame]:
        response = requests.get(self.modifier_url, headers=self.pom_auth_headers)
        # Check if the request was successful
        modifier_df = pd.DataFrame()
        if response.status_code != 200:
            logger.error(f"Recieved response code {response} when retrieving modifiers")
            response.raise_for_status()
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

    def _get_item_base_types(self) -> dict[str, int]:
        response = requests.get(self.item_base_type_url, headers=self.pom_auth_headers)
        item_base_type_mapped = {}
        item_base_types = []

        if response.status_code != 200:
            logger.error(
                f"Recieved response code {response} when retrieving item base types"
            )
            response.raise_for_status()

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

    def _get_new_currency_data(self) -> pd.DataFrame:
        currency_df = self.poe_ninja_currency_api_handler.make_request()
        currency_df = self.poe_ninja_transformer.transform_into_tables(currency_df)
        return currency_df

    def _initialize_data_stream_threads(
        self, executor: ThreadPoolExecutor, listeners: int, has_crashed: bool = False
    ) -> dict[Future, str]:
        return self.poe_api_handler.initialize_data_stream_threads(
            executor, listeners, has_crashed
        )

    def _follow_data_dump_stream(self):
        try:
            logger.info("Retrieving modifiers from db.")
            modifier_dfs = self._get_modifiers()
            item_base_types = self._get_item_base_types()
            get_df = self.poe_api_handler.dump_stream()
            for i, df in enumerate(get_df):
                split_dfs = self._categorize_new_items(df)
                if i % 50 == 0:
                    currency_df = self._get_new_currency_data()
                for data_transformer_type in self.data_transformers:
                    self.data_transformers[data_transformer_type].transform_into_tables(
                        df=split_dfs[data_transformer_type],
                        modifier_df=modifier_dfs[data_transformer_type],
                        currency_df=currency_df.copy(deep=True),
                        item_base_types=item_base_types,
                    )
        except Exception as e:
            logger.exception(
                f"The following exception occured during '_follow_data_dump_stream': {e}"
            )
            raise

    def retrieve_data(self):
        logger.info("Program starting up.")
        logger.info("Initiating data stream.")
        max_workers = 3
        listeners = max_workers - 1  # minus one because of transformation threads
        try:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = self._initialize_data_stream_threads(
                    executor, listeners=listeners
                )
                follow_future = executor.submit(self._follow_data_dump_stream)
                futures[follow_future] = "data_processing"
                logger.info("Waiting for futures to crash.")
                while True:
                    done_futures, not_done_futures = wait(
                        futures, return_when=FIRST_EXCEPTION
                    )
                    crashed_future = list(done_futures)[0]
                    future_job = futures.pop(crashed_future)
                    logger.info(
                        f"The future '{future_job}' has crashed. Finding exception..."
                    )
                    if future_job == "data_processing":
                        crashed_future_exception = crashed_future.exception()
                        try:
                            raise crashed_future_exception
                        except ProgramTooSlowException:
                            logger.info(
                                f"The job '{future_job}' was too slow. Restarting..."
                            )
                            self.poe_api_handler.set_program_too_slow()

                            wait(futures, return_when=ALL_COMPLETED)

                            raise ProgramTooSlowException
                        except ProgramRunTooLongException:
                            logger.info(
                                f"The job '{future_job}' has been running too long. Restarting..."
                            )
                            self.poe_api_handler.set_program_too_slow()

                            wait(futures, return_when=ALL_COMPLETED)
                            raise ProgramRunTooLongException
                        except Exception:
                            logger.exception(
                                f"The following exception occured in job '{future_job}': {crashed_future_exception}"
                            )
                            follow_future = executor.submit(
                                self._follow_data_dump_stream
                            )
                            futures[follow_future] = "data_processing"
                    elif future_job == "listener":
                        print(crashed_future_exception)
                        raise Exception("OLLLAH")
                        new_future = self._initialize_data_stream_threads(
                            executor,
                            listeners=1,
                            has_crashed=True,
                        )
                        futures[new_future] = "listener"
        except ProgramTooSlowException:
            logger.info("Program was too slow. Restarting...")
        except ProgramRunTooLongException:
            logger.info("Program has run too long. Restarting...")
        except Exception as e:
            logger.exception(f"The following exception occured: {e}")
            raise e


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
