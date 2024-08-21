from __future__ import annotations

from fastapi import APIRouter, Depends

import app.plotting.schemas as schemas
from app.api.deps import SessionDep, get_current_active_user
from app.plotting import plotter_tool

router = APIRouter()


plot_prefix = "plot"


@router.post(
    "/",
    response_model=schemas.PlotData,
    dependencies=[Depends(get_current_active_user)],
)
async def get_plot_data(
    query: schemas.PlotQuery,
    db: SessionDep,
):
    """
    Takes a query based on the 'PlotQuery' schema and retrieves data
    to be used for plotting in the format of the 'PlotData' schema.

    The 'PlotQuery' schema allows for modifier restriction and item specifications.
    """

    return await plotter_tool.plot(db, query=query)
