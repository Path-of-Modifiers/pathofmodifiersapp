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


uvicorn_access = logging.getLogger("uvicorn.access")
uvicorn_access.disabled = True

logger = logging.getLogger("uvicorn")

setup_logging()

logging.basicConfig(level="INFO")

logger.setLevel(logging.INFO)
