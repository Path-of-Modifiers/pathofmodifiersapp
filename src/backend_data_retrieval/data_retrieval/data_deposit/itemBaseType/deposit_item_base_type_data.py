import logging

from pandas import DataFrame
from data_deposit.deposit_base import DataDepositerBase

logging.basicConfig(
    filename="modifier_data_deposit.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)-8s:%(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class ItemBaseTypeDataDepositer(DataDepositerBase):
    def __init__(self, logger: logging.Logger) -> None:
        super().__init__(data_type="itemBaseType", logger=logger)

    def _process_data(self, df: DataFrame) -> DataFrame:
        return df
