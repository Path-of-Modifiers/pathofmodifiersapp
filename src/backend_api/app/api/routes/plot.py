from fastapi import APIRouter, Depends, Request
from starlette_context import context
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    UserCacheSession,
    get_async_current_active_user,
    get_async_db,
    get_rate_limit_tier_by_request,
    get_username_by_request,
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
    dependencies=[Depends(get_async_current_active_user)],
)
async def get_plot_data(
    request: Request,
    query: PlotQuery,
    user_cache_session: UserCacheSession,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Takes a query based on the 'PlotQuery' schema and retrieves data
    to be used for plotting in the format of the 'PlotData' schema.

    The 'PlotQuery' schema allows for modifier restriction and item specifications.
    """
    rate_limit_tier = await get_rate_limit_tier_by_request(request, user_cache_session)
    rate_spec = RateSpec(
        requests=rate_limit_tier,
        cooldown_seconds=rate_limit_settings.PLOT_RATE_LIMIT_COOLDOWN_SECONDS,
    )

    async with apply_custom_rate_limit(
        unique_key="plot_" + get_username_by_request(request),
        rate_spec=rate_spec,
        prefix=plot_prefix,
    ), apply_custom_rate_limit(
        unique_key="plot_" + context.data["X-Forwarded-For"],
        rate_spec=rate_spec,
        prefix=plot_prefix,
    ):
        plot_data = await plotter_tool.plot(
            db,
            query=query,
        )
        return plot_data
