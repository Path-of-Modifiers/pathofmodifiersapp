from backend_api.app.api.routes import (
    currency,
    currency_prefix,
    item,
    item_base_type,
    item_base_type_prefix,
    item_prefix,
    league,
    league_prefix,
    login,
    login_prefix,
    modifier,
    modifier_prefix,
    plot,
    plot_prefix,
    table_version,
    table_version_prefix,
    test,
    test_prefix,
    turnstile,
    turnstile_prefix,
    unidentified_item,
    unidentified_item_prefix,
    unique_item,
    unique_item_prefix,
)
from fastapi import APIRouter

api_router = APIRouter()


api_router.include_router(
    currency.router, prefix=f"/{currency_prefix}", tags=[currency_prefix]
)
api_router.include_router(
    item_base_type.router,
    prefix=f"/{item_base_type_prefix}",
    tags=[item_base_type_prefix],
)
api_router.include_router(item.router, prefix=f"/{item_prefix}", tags=[item_prefix])
api_router.include_router(
    league.router, prefix=f"/{league_prefix}", tags=[league_prefix]
)
api_router.include_router(
    unidentified_item.router,
    prefix=f"/{unidentified_item_prefix}",
    tags=[unidentified_item_prefix],
)
api_router.include_router(
    modifier.router, prefix=f"/{modifier_prefix}", tags=[modifier_prefix]
)
api_router.include_router(
    unique_item.router, prefix=f"/{unique_item_prefix}", tags=[unique_item_prefix]
)
api_router.include_router(plot.router, prefix=f"/{plot_prefix}", tags=[plot_prefix])
api_router.include_router(
    turnstile.router, prefix=f"/{turnstile_prefix}", tags=[turnstile_prefix]
)
api_router.include_router(test.router, prefix=f"/{test_prefix}", tags=[test_prefix])
api_router.include_router(
    login.router,
    prefix=f"/{login_prefix}",
    tags=[login_prefix],
)

api_router.include_router(
    table_version.router,
    prefix=f"/{table_version_prefix}",
    tags=[table_version_prefix],
)
