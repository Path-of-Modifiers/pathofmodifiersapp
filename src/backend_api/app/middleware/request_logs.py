import http
import time

from fastapi import Request

from app.api.deps import (
    get_user_ip_from_header,
)
from app.logs.logger import logger_request

"""
Taken from https://medium.com/@roy-pstr/fastapi-server-errors-and-logs-take-back-control-696405437983
"""


async def log_request_middleware(request: Request, call_next):
    """
    This middleware will log all requests and their processing time.
    E.g. log:
    0.0.0.0:1234 - GET /ping 200 OK 1.00ms
    """
    url = (
        f"{request.url.path}?{request.query_params}"
        if request.query_params
        else request.url.path
    )
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = f"{process_time:.2f}"
    host = get_user_ip_from_header(request)
    port = getattr(getattr(request, "client", None), "port", None)
    try:
        status_phrase = http.HTTPStatus(response.status_code).phrase
    except ValueError:
        status_phrase = ""
    logger_object = (
        f"host={host} "
        f"port={port} "
        f"method={request.method} "
        f"url={url} "
        f"status_code={response.status_code} "
        f"""status_phrase="{status_phrase}" """
        f"process_time_ms={formatted_process_time}"
    )

    logger_request.info(logger_object)
    if process_time > 10000:
        logger_request.warning("Request took longer than 10 seconds.")
    return response
