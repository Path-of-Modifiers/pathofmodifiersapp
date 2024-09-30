from typing import Literal

from deposit_base import DataDepositerBase
from itemBaseType.deposit_item_base_type_data import ItemBaseTypeDataDepositer
from modifier.deposit_modifier_data import ModifierDataDepositer

from logs.logger import data_deposit_logger as logger
from logs.logger import setup_logging


def main():
    setup_logging()
    logger.info("Starting deposit phase.")
    data_depositers: dict[Literal["modifier", "itemBaseType"], DataDepositerBase] = {
        "modifer": ModifierDataDepositer(logger),
        "itemBaseType": ItemBaseTypeDataDepositer(logger),
    }
    for key, data_depositer in data_depositers.items():
        logger.info(f"Depositing {key} data.")
        data_depositer.deposit_data()
    return 0


if __name__ == "__main__":
    main()
