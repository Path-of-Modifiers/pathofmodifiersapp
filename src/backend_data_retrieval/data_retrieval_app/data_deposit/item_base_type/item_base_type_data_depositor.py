from pandas import DataFrame

from data_retrieval_app.data_deposit.data_depositor_base import DataDepositorBase


class ItemBaseTypeDataDepositor(DataDepositorBase):
    def __init__(self) -> None:
        super().__init__(data_type="item_base_type")

        self.data_url += "?on_duplicate_pkey_do_nothing=true"

    def _process_data(self, df: DataFrame) -> DataFrame:
        return df
