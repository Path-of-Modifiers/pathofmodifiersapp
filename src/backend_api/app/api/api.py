from fastapi import APIRouter

from app.api.routes import (
    currency,
    currency_prefix,
    item,
    item_base_type,
    item_base_type_prefix,
    item_modifier,
    item_modifier_prefix,
    item_prefix,
    login,
    login_prefix,
    modifier,
    modifier_prefix,
    plot,
    plot_prefix,
    test,
    test_prefix,
    turnstile,
    turnstile_prefix,
    unidentified_item,
    unidentified_item_prefix,
)

api_router = APIRouter()


api_router.include_router(
    currency.router, prefix=f"/{currency_prefix}", tags=[f"{currency_prefix}s"]
)
api_router.include_router(
    item_base_type.router,
    prefix=f"/{item_base_type_prefix}",
    tags=[f"{item_base_type_prefix}s"],
)
api_router.include_router(
    item_modifier.router,
    prefix=f"/{item_modifier_prefix}",
    tags=[f"{item_modifier_prefix}s"],
)
api_router.include_router(
    item.router, prefix=f"/{item_prefix}", tags=[f"{item_prefix}s"]
)
api_router.include_router(
    unidentified_item.router,
    prefix=f"/{unidentified_item_prefix}",
    tags=[f"{unidentified_item_prefix}s"],
)
api_router.include_router(
    modifier.router, prefix=f"/{modifier_prefix}", tags=[f"{modifier_prefix}s"]
)
api_router.include_router(
    plot.router, prefix=f"/{plot_prefix}", tags=[f"{plot_prefix}s"]
)
api_router.include_router(
    turnstile.router, prefix=f"/{turnstile_prefix}", tags=[f"{turnstile_prefix}s"]
)
api_router.include_router(
    test.router, prefix=f"/{test_prefix}", tags=[f"{test_prefix}s"]
)
api_router.include_router(
    login.router,
    prefix=f"/{login_prefix}",
    tags=[f"{login_prefix}s"],
)
