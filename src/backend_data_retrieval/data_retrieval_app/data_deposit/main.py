from typing import Literal

from data_retrieval_app.data_deposit.deposit_base import DataDepositerBase
from data_retrieval_app.data_deposit.item_base_type.deposit_item_base_type_data import (
    ItemBaseTypeDataDepositer,
)
from data_retrieval_app.data_deposit.modifier.deposit_modifier_data import (
    ModifierDataDepositer,
)
from data_retrieval_app.logs.logger import data_deposit_logger as logger
from data_retrieval_app.logs.logger import setup_logging


def main():
    setup_logging()
    logger.info("Starting deposit phase.")
    data_depositers: dict[Literal["modifier", "itemBaseType"], DataDepositerBase] = {
        "modifer": ModifierDataDepositer(),
        "itemBaseType": ItemBaseTypeDataDepositer(),
    }
    for key, data_depositer in data_depositers.items():
        logger.info(f"Depositing {key} data.")
        data_depositer.deposit_data()
    return 0


if __name__ == "__main__":
    main()
