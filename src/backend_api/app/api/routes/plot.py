from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    UserCacheSession,
    async_get_current_active_user,
    get_async_db,
    get_rate_limit_tier_by_request,
    get_username_by_request,
)
from app.api.rate_limit.rate_limiter import RateLimiter, RateSpec
from app.core.cache.cache import cache
from app.core.config import settings
from app.core.schemas.plot import PlotData, PlotQuery
from app.plotting import plotter_tool

router = APIRouter()

plot_prefix = "plot"


@router.post(
    "/",
    response_model=PlotData,
    dependencies=[Depends(async_get_current_active_user)],
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

    async with RateLimiter(
        unique_key=get_username_by_request(request),
        backend=cache,
        rate_spec=RateSpec(
            requests=await get_rate_limit_tier_by_request(request, user_cache_session),
            cooldown_seconds=settings.PLOT_RATE_LIMIT_COOLDOWN_SECONDS,
        ),
        cache_prefix=plot_prefix,
        enabled=settings.RATE_LIMIT,
    ):
        return await plotter_tool.plot(
            db,
            query=query,
        )
