import logging

"""
Taken from https://medium.com/@roy-pstr/fastapi-server-errors-and-logs-take-back-control-696405437983
"""

# Disable uvicorn access logger
uvicorn_access = logging.getLogger("uvicorn.access")
uvicorn_access.disabled = True

logger = logging.getLogger("uvicorn")
logging.basicConfig(filename="backend_api.log", encoding="utf-8", level=logging.INFO)
