from __future__ import annotations
from fastapi import APIRouter, Depends
from typing import List, Optional, Union

from app.api.deps import get_db

from app.plotting import plotter_tool

import app.plotting.schemas as schemas

from sqlalchemy.orm import Session

from app.core.security import verification


router = APIRouter()


plot_prefix = "plot"


@router.post("/", response_model=schemas.PlotData)
async def get_plot_data(
    query: schemas.PlotQuery,
    db: Session = Depends(get_db),
):
    """
    Takes a query based on the 'PlotQuery' schema and retrieves data
    to be used for plotting in the format of the 'PlotData' schema.

    The 'PlotQuery' schema allows for modifier restriction and item specifications.
    """

    return await plotter_tool.plot(db, query=query)
