from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_async_db,
    get_user_ip_from_header,
)
from app.core.rate_limit.custom_rate_limiter import RateSpec
from app.core.rate_limit.rate_limit_config import rate_limit_settings
from app.core.rate_limit.rate_limiters import apply_custom_rate_limit
from app.core.schemas.plot import PlotData, PlotQuery
from app.plotting import configure_plotter_by_query, plotter_service

router = APIRouter()

plot_prefix = "plot"


def _get_ratespec_ip(request: Request) -> tuple[RateSpec, str]:
    request_limit = rate_limit_settings.TIER_0_PLOT_RATE_LIMIT
    rate_spec = RateSpec(
        requests=request_limit,
        cooldown_seconds=rate_limit_settings.PLOT_RATE_LIMIT_COOLDOWN_SECONDS,
    )

    client_ip = get_user_ip_from_header(request)
    return rate_spec, client_ip


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

    rate_spec, client_ip = _get_ratespec_ip(request)

    async with apply_custom_rate_limit(
        unique_key="plot_" + client_ip,
        rate_spec=rate_spec,
        prefix=plot_prefix,
    ):
        plotter = configure_plotter_by_query(query)
        plot_data = await plotter_service.plot(
            plotter,
            db,
            query=query,
        )
        return plot_data
