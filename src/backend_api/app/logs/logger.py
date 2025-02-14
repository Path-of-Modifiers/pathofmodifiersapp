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


logger = logging.getLogger("pom_app")

logger_request = logging.getLogger("pom_app.request")

plot_logger = logging.getLogger("pom_app.plot")

test_logger = logging.getLogger("pom_app.test")
