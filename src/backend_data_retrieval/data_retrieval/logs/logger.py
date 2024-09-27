import logging
import logging.config
from pathlib import Path

import yaml


def setup_logging():
    # Determine the path to config.yml relative to the current directory
    config_path = Path(__file__).parent / "config" / "config.yml"

    # Load YAML configuration
    with open(config_path) as f_in:
        config = yaml.safe_load(f_in)

    # Apply logging configuration
    logging.config.dictConfig(config)


main_logger = logging.getLogger("data-retrieval")

external_data_retrieval_logger = main_logger.getChild("external-data-retrieval")

transform_logger = external_data_retrieval_logger.getChild("transform")

data_retrieval_logger = external_data_retrieval_logger.getChild("data-retrieval")

modifier_data_deposit_logger = main_logger.getChild("modifier-data-deposit")
