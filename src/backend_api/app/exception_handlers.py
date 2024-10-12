import sys

from fastapi import Request
from fastapi.exception_handlers import http_exception_handler as _http_exception_handler
from fastapi.exception_handlers import (
    request_validation_exception_handler as _request_validation_exception_handler,
)
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse, Response
from slowapi.errors import RateLimitExceeded

from app.exceptions.model_exceptions.plot_exception import RateLimitExceededError
from app.logs.logger import logger

"""
Taken from https://medium.com/@roy-pstr/fastapi-server-errors-and-logs-take-back-control-696405437983

"""


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    This is a wrapper to the default RequestValidationException handler of FastAPI.
    This function will be called when client input is not valid.
    """
    logger.debug("Our custom request_validation_exception_handler was called")
    body = await request.body()
    query_params = request.query_params._dict  # pylint: disable=protected-access
    detail = {
        "errors": exc.errors(),
        "body": body.decode(),
        "query_params": query_params,
    }
    logger.info(detail)
    return await _request_validation_exception_handler(request, exc)


async def http_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse | Response:
    """
    This is a wrapper to the default HTTPException handler of FastAPI.
    This function will be called when a HTTPException is explicitly raised.
    """
    logger.debug("Our custom http_exception_handler was called")
    return await _http_exception_handler(request, exc)


async def unhandled_exception_handler(
    request: Request, exc: Exception
) -> PlainTextResponse:
    """
    This middleware will log all unhandled exceptions.
    Unhandled exceptions are all exceptions that are not HTTPExceptions or RequestValidationErrors.
    """
    logger.debug("Our custom unhandled_exception_handler was called")
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    url = (
        f"{request.url.path}?{request.query_params}"
        if request.query_params
        else request.url.path
    )
    exception_type, exception_value, exception_traceback = sys.exc_info()
    exception_name = getattr(exception_type, "__name__", None)
    logger.error(
        f'{host}:{port} - "{request.method} {url}" 500 Internal Server Error <{exception_name}: {exception_value}>'
    )
    return PlainTextResponse(str(exc), status_code=500)


async def slow_api_rate_limit_exceeded_handler(
    request: Request,  # noqa: ARG001
    exc: RateLimitExceeded,
):
    retry_after_seconds = exc.limit.limit.get_expiry()
    max_amount_of_tries_per_time_period = exc.detail

    response_body = {
        "detail": f"POM API : Rate limit exceeded. Please try again later. "
        f"max_tries: {max_amount_of_tries_per_time_period}s"
    }

    return JSONResponse(
        status_code=429,
        content=response_body,
        headers={"Retry-After-Seconds": str(retry_after_seconds)},
    )


async def custom_rate_limit_exceeded_handler(
    request: Request,  # noqa: ARG001
    exc: RateLimitExceededError,
):
    retry_after_seconds = exc.headers["Retry-After-Seconds"]

    response_body = {"detail": exc.detail}

    return JSONResponse(
        status_code=exc.status_code,
        content=response_body,
        headers={"Retry-After-Seconds": str(retry_after_seconds)},
    )
