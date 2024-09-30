import logging

from pandas import DataFrame

from data_deposit.deposit_base import DataDepositerBase


class ItemBaseTypeDataDepositer(DataDepositerBase):
    def __init__(self, logger: logging.Logger) -> None:
        super().__init__(data_type="itemBaseType", logger=logger)

        self.data_url += "?on_duplicate_pkey_do_nothing=true"

    def _process_data(self, df: DataFrame) -> DataFrame:
        return df
