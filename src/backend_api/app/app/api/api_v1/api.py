from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    account,
    currency,
    item_base_type,
    item_modifier,
    item,
    modifier,
    stash,
    plot,
    account_prefix,
    currency_prefix,
    item_base_type_prefix,
    item_modifier_prefix,
    item_prefix,
    modifier_prefix,
    stash_prefix,
    plot_prefix,
)

api_router = APIRouter()


api_router.include_router(
    account.router, prefix=f"/{account_prefix}", tags=[f"{account_prefix}s"]
)
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
    modifier.router, prefix=f"/{modifier_prefix}", tags=[f"{modifier_prefix}s"]
)
api_router.include_router(
    stash.router, prefix=f"/{stash_prefix}", tags=[f"{stash_prefix}s"]
)
api_router.include_router(
    plot.router, prefix=f"/{plot_prefix}", tags=[f"{plot_prefix}s"]
)
