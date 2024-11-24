from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    UserCacheSession,
    get_async_db,
    get_rate_limit_tier_by_request,
    get_user_ip_from_header,
)
from app.core.rate_limit.custom_rate_limiter import RateSpec
from app.core.rate_limit.rate_limit_config import rate_limit_settings
from app.core.rate_limit.rate_limiters import apply_custom_rate_limit
from app.core.schemas.plot import PlotData, PlotQuery
from app.plotting import plotter_tool

router = APIRouter()

plot_prefix = "plot"


@router.post(
    "/",
    response_model=PlotData,
)
async def get_plot_data(
    request: Request,
    query: PlotQuery,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Takes a query based on the 'PlotQuery' schema and retrieves data
    to be used for plotting in the format of the 'PlotData' schema.

    The 'PlotQuery' schema allows for modifier restriction and item specifications.
    """
    request_limit = 4
    rate_spec = RateSpec(
        requests=request_limit,
        cooldown_seconds=rate_limit_settings.PLOT_RATE_LIMIT_COOLDOWN_SECONDS,
    )

    client_ip = get_user_ip_from_header(request)

    async with apply_custom_rate_limit(
        unique_key="plot_" + client_ip,
        rate_spec=rate_spec,
        prefix=plot_prefix,
    ):
        plot_data = await plotter_tool.plot(
            db,
            query=query,
        )
        return plot_data
