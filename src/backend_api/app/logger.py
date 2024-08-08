import logging

# Disable uvicorn access logger
uvicorn_access = logging.getLogger("uvicorn.access")
uvicorn_access.disabled = True

logger = logging.getLogger("uvicorn")
logging.basicConfig(filename="backend_api.log", encoding="utf-8", level=logging.INFO)
