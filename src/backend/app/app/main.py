from __future__ import annotations
from fastapi import FastAPI

from app.api.api_v1.api import api_router

from app.core.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    # generate_unique_id_function=custom_generate_unique_id,
)


@app.get("/")
async def read_main():
    return {"message": "Welcome to Path of Modifiers API!"}


app.include_router(api_router, prefix=settings.API_V1_STR)
