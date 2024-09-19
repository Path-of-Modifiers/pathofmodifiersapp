import logging
import sys

"""
Taken from https://medium.com/@roy-pstr/fastapi-server-errors-and-logs-take-back-control-696405437983
"""

# Disable uvicorn access logger
uvicorn_access = logging.getLogger("uvicorn.access")
uvicorn_access.disabled = True

logger = logging.getLogger("uvicorn")

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("backend_api.log")

stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.handlers = [stream_handler, file_handler]

logger.setLevel(logging.INFO)
