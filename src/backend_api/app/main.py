from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from slowapi.errors import RateLimitExceeded
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.api.api import api_router
from app.core.config import settings
from app.core.models.database import async_engine
from app.exception_handlers import (
    custom_rate_limit_exceeded_handler,
    http_exception_handler,
    request_validation_exception_handler,
    slow_api_rate_limit_exceeded_handler,
    unhandled_exception_handler,
)
from app.exceptions.model_exceptions.rate_limit_exception import RateLimitExceededError
from app.logs.logger import setup_logging
from app.middleware.request_logs import log_request_middleware


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    # Load the ML model
    setup_logging()
    yield
    await async_engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(api_router, prefix=settings.API_V1_STR)

"""
Taken from https://medium.com/@roy-pstr/fastapi-server-errors-and-logs-take-back-control-696405437983
"""
app.middleware("http")(log_request_middleware)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
app.add_exception_handler(RateLimitExceeded, slow_api_rate_limit_exceeded_handler)
app.add_exception_handler(RateLimitExceededError, custom_rate_limit_exceeded_handler)

app.add_middleware(ProxyHeadersMiddleware)
