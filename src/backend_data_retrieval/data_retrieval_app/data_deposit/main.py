from typing import Literal

from data_retrieval_app.data_deposit.data_depositor_base import DataDepositorBase
from data_retrieval_app.data_deposit.item_base_type.item_base_type_data_depositor import (
    ItemBaseTypeDataDepositor,
)
from data_retrieval_app.data_deposit.modifier.modifier_data_depositor import (
    ModifierDataDepositor,
)
from data_retrieval_app.logs.logger import data_deposit_logger as logger
from data_retrieval_app.logs.logger import setup_logging


def main():
    setup_logging()
    logger.info("Starting deposit phase.")
    data_depositors: dict[Literal["modifier", "itemBaseType"], DataDepositorBase] = {
        "modifer": ModifierDataDepositor(),
        "itemBaseType": ItemBaseTypeDataDepositor(),
    }
    for key, data_depositor in data_depositors.items():
        logger.info(f"Depositing {key} data.")
        data_depositor.deposit_data()
    return 0


if __name__ == "__main__":
    main()
