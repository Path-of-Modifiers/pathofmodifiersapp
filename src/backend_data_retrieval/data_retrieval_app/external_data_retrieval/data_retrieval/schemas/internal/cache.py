from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.external.poe import (
    PoeModel,
)


class CacheItem(PoeModel):
    id: str
    note: str
    category: str


class CacheItemWithContext(CacheItem):
    league: str


class CacheStash(PoeModel):
    league: str
    items: list[CacheItem]
