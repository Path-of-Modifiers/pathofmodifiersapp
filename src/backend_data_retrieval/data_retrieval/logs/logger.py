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


main_logger = logging.getLogger("dataret")

external_data_retrieval_logger = main_logger.getChild("ext")

transform_logger = external_data_retrieval_logger.getChild("transform")

data_retrieval_logger = external_data_retrieval_logger.getChild("dataret")

data_deposit_logger = main_logger.getChild("datadepo")
