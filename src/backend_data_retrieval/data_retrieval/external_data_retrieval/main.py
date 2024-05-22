import requests
import logging
import os
import pandas as pd
from typing import Dict, Optional

from external_data_retrieval.data_retrieval.poe_api_retrieval.poe_api import (
    APIHandler,
)
from external_data_retrieval.data_retrieval.poe_ninja_currency_retrieval.poe_ninja_currency_api import (
    PoeNinjaCurrencyAPIHandler,
)
from external_data_retrieval.transforming_data.transform_poe_ninja_currency_api_data import (
    TransformPoeNinjaCurrencyAPIData,
)
from external_data_retrieval.transforming_data.transform_poe_api_data import (
    PoeAPIDataTransformer,
    UniquePoeAPIDataTransformer,
)

logger = logging.getLogger("external_data_retrieval")
logging.basicConfig(
    filename="external_data_retrieval.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)-8s:%(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

BASEURL = os.getenv("DOMAIN")
POE_PUBLIC_STASHES_AUTH_TOKEN = os.getenv("POE_PUBLIC_STASHES_AUTH_TOKEN")


class ContiniousDataRetrieval:
    auth_token = POE_PUBLIC_STASHES_AUTH_TOKEN
    url = "https://api.pathofexile.com/public-stash-tabs"

    if "localhost" not in BASEURL:
        base_pom_api_url = f"https://{BASEURL}"
    else:
        base_pom_api_url = "http://src-backend-1"
    modifier_url = base_pom_api_url + "/api/api_v1/modifier/"

    def __init__(
        self,
        items_per_batch: int,
        data_transformers: Dict[str, PoeAPIDataTransformer],
        logger: logging.Logger,
    ):

        self.data_transformers = {
            key: data_transformers[key](main_logger=logger) for key in data_transformers
        }

        self.poe_api_handler = APIHandler(
            url=self.url,
            auth_token=self.auth_token,
            logger_parent=logger,
            n_wanted_items=items_per_batch,
            n_unique_wanted_items=10,
        )

        self.poe_ninja_currency_api_handler = PoeNinjaCurrencyAPIHandler(
            url="https://poe.ninja/api/data/currencyoverview?league=Necropolis&type=Currency"
        )
        self.poe_ninja_transformer = TransformPoeNinjaCurrencyAPIData(
            logger_parent=logger
        )

        self.logger = logger

    def _get_modifiers(self) -> Dict[str, pd.DataFrame]:

        modifier_df = pd.read_json(self.modifier_url, dtype=str)
        modifier_types = [
            "implicit",
            "explicit",
            "delve",
            "fractured",
            "synthesized",
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

    def _categorize_new_items(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        split_dfs = {}

        # TODO not fully exhaustive yet, needs to be updated over time
        category_priority = [
            # "synthesized",
            # "fractured",
            # "delve",
            # "veiled",
            "unique",
        ]
        # Needs to take priority, see nebulis and rational doctrine
        # not_synth_mask = df["synthesized"].isna()
        # split_dfs["synthesized"] = df.loc[~not_synth_mask]
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

    def retrieve_data(self):
        self.logger.info("Program starting up.")
        self.logger.info("Retrieving modifiers from db.")
        modifier_dfs = self._get_modifiers()
        self.logger.info("Initiating data stream.")
        get_df = self.poe_api_handler.dump_stream()
        for i, df in enumerate(get_df):
            split_dfs = self._categorize_new_items(df)
            if i % 10 == 0:
                currency_df = self._get_new_currency_data()
            for data_transformer_type in self.data_transformers:
                self.data_transformers[data_transformer_type].transform_into_tables(
                    df=split_dfs[data_transformer_type],
                    modifier_df=modifier_dfs[data_transformer_type],
                    currency_df=currency_df.copy(deep=True),
                )


def main():
    auth_token = POE_PUBLIC_STASHES_AUTH_TOKEN
    url = "https://api.pathofexile.com/public-stash-tabs"

    items_per_batch = 300
    data_transformers = {"unique": UniquePoeAPIDataTransformer}

    data_retriever = ContiniousDataRetrieval(
        items_per_batch=items_per_batch,
        data_transformers=data_transformers,
        logger=logger,
    )

    data_retriever.retrieve_data()
    # data_retriever.retrieve_data()


if __name__ == "__main__":
    main()
