from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.base import (
    PoeModel,
)


class CacheItem(PoeModel):
    id: str
    note: str
    category: str

    def add_context(self, league: str) -> "CacheItemWithContext":
        return CacheItemWithContext(
            id=self.id, note=self.note, category=self.category, league=league
        )


class CacheItemWithContext(CacheItem):
    league: str


class CacheStash(PoeModel):
    league: str
    items: list[CacheItem]
