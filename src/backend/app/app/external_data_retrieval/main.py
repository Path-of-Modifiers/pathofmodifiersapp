import asyncio
import os
import requests
import pandas as pd
from typing import List, Union, Dict

from app.external_data_retrieval.data_retrieval.poe_api_retrieval.poe_api import (
    APIHandler,
)
from app.external_data_retrieval.transforming_data.transforming_dynamic_data.transform_poe_api_data import (
    PoeAPIDataTransformer,
    UniquePoeAPIDataTransformer,
)

BASEURL = os.getenv("DOMAIN")


class ContiniousDataRetrieval:
    auth_token = "750d4f685cfa83d024d86508e7ede4ab55b5acc7"
    url = "https://api.pathofexile.com/public-stash-tabs"
    modifier_url = BASEURL + "/api/api_v1/modifier/"

    def __init__(
        self, items_per_batch: int, data_transformers: Dict[str, PoeAPIDataTransformer]
    ):
        self.data_transformers = data_transformers

        self.api_handler = APIHandler(
            url=self.url,
            auth_token=self.auth_token,
            n_wanted_items=items_per_batch,
            n_unique_wanted_items=10,
        )

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

    def retrieve_data(self, initial_next_change_id: str):
        modifier_dfs = self._get_modifiers()
        get_df = self.api_handler.dump_stream(
            initial_next_change_id=initial_next_change_id
        )
        for i, df in enumerate(get_df):
            split_dfs = self._categorize_new_items(df)
            for data_transformer_type in self.data_transformers:
                self.data_transformers[data_transformer_type].transform_into_tables(
                    df=split_dfs[data_transformer_type],
                    modifier_df=modifier_dfs[data_transformer_type],
                )


def main():
    auth_token = "750d4f685cfa83d024d86508e7ede4ab55b5acc7"
    url = "https://api.pathofexile.com/public-stash-tabs"

    n_wanted_items = 3000
    data_transformers = {"unique": UniquePoeAPIDataTransformer()}

    data_retriever = ContiniousDataRetrieval(
        items_per_batch=n_wanted_items, data_transformers=data_transformers
    )
    data_retriever.retrieve_data(
        initial_next_change_id="2304265269-2292493816-2218568823-2460180973-2390424272"
    )
    # n_unique_wanted_items = 15

    # api_handler = APIHandler(
    #     url=url,
    #     auth_token=auth_token,
    #     n_wanted_items=n_wanted_items,
    #     n_unique_wanted_items=n_unique_wanted_items,
    # )
    # for df in api_handler.dump_stream(
    #     initial_next_change_id="2304265269-2292493816-2218568823-2460180973-2390424272"
    # ):  # From poe.ninja
    #     # print(df)
    #     # df.to_csv("test.csv", index=False)
    #     quit()

    # return 0


if __name__ == "__main__":
    main()
