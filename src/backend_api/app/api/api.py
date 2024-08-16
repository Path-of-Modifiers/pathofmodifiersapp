from fastapi import APIRouter

from app.api.routes import (
    account,
    currency,
    item_base_type,
    item_modifier,
    item,
    login,
    modifier,
    stash,
    plot,
    turnstile,
    user,
    temporary_hashed_user_ip,
    account_prefix,
    currency_prefix,
    item_base_type_prefix,
    item_modifier_prefix,
    item_prefix,
    login_prefix,
    modifier_prefix,
    stash_prefix,
    plot_prefix,
    turnstile_prefix,
    user_prefix,
    temporary_hashed_user_ip_prefix,
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
    login.router, prefix=f"/{login_prefix}", tags=[f"{login_prefix}s"]
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
api_router.include_router(
    temporary_hashed_user_ip.router,
    prefix=f"/{temporary_hashed_user_ip_prefix}",
    tags=[f"{temporary_hashed_user_ip_prefix}s"],
)
api_router.include_router(
    turnstile.router, prefix=f"/{turnstile_prefix}", tags=[f"{turnstile_prefix}s"]
)
api_router.include_router(
    user.router, prefix=f"/{user_prefix}", tags=[f"{user_prefix}s"]
)
