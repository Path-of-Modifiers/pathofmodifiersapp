from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    account,
    currency,
    item_base_type,
    item_modifier,
    item,
    modifier,
    stash,
)

api_router = APIRouter()

api_router.include_router(account.router, prefix="/account", tags=["accounts"])
api_router.include_router(currency.router, prefix="/currency", tags=["currencies"])
api_router.include_router(
    item_base_type.router, prefix="/itemBaseType", tags=["itemBaseTypes"]
)
api_router.include_router(
    item_modifier.router, prefix="/itemModifier", tags=["itemModifiers"]
)
api_router.include_router(item.router, prefix="/item", tags=["items"])
api_router.include_router(modifier.router, prefix="/modifier", tags=["modifiers"])
api_router.include_router(stash.router, prefix="/stash", tags=["stashes"])
