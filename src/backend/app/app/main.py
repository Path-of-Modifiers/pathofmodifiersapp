from __future__ import annotations
from fastapi import FastAPI, Depends
from typing import List, Union, Optional

from app.api.api_v1.api import api_router
import app.core.models.models as _models
import app.api.deps as _deps

import app.crud as _crud

import app.core.schemas as _schemas

from app.core.config import settings


import sqlalchemy.orm as _orm

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    # generate_unique_id_function=custom_generate_unique_id,
)


@app.get("/")
async def read_main():
    return {"message": "Welcome to Path of Modifiers API!"}


app.include_router(api_router, prefix=settings.API_V1_STR)
