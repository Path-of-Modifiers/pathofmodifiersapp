from __future__ import annotations

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.core.config import settings
from app.limiter import apply_ip_rate_limits
from app.plotting import plotter_tool
from app.plotting.schemas.input import PlotQuery
from app.plotting.schemas.output import PlotData

router = APIRouter()


plot_prefix = "plot"


@router.post(
    "/",
    response_model=PlotData,
    dependencies=[Depends(get_current_active_user)],
)
@apply_ip_rate_limits(
    settings.TIER_0_PLOT_RATE_LIMIT_SECOND,
    settings.TIER_0_PLOT_RATE_LIMIT_MINUTE,
    settings.TIER_0_PLOT_RATE_LIMIT_HOUR,
    settings.TIER_0_PLOT_RATE_LIMIT_DAY,
)
async def get_plot_data(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    query: PlotQuery,
    db: Session = Depends(get_db),
):
    """
    Takes a query based on the 'PlotQuery' schema and retrieves data
    to be used for plotting in the format of the 'PlotData' schema.

    The 'PlotQuery' schema allows for modifier restriction and item specifications.
    """

    return await plotter_tool.plot(db, query=query)
