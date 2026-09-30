from pydantic import Field

from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.base import (
    PoeModel,
)
from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.external.poe import (
    PoeItem,
)
from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.internal.cache import (
    CacheItemWithContext,
)


class OrganizedItems(PoeModel):
    removed_items: list[CacheItemWithContext] = Field(default_factory=list)
    changed_items: list[PoeItem] = Field(default_factory=list)
    new_items: list[PoeItem] = Field(default_factory=list)

    def extend(self, table: "OrganizedItems"):
        self.removed_items.extend(table.removed_items)
        self.changed_items.extend(table.changed_items)
        self.new_items.extend(table.new_items)

    def is_empty(self) -> bool:
        return not (self.removed_items or self.changed_items or self.new_items)


class OrganizedItemsByCategory(PoeModel):
    """
    Field names much match the identifiers of the category detectors
    """

    unique: OrganizedItems = Field(default_factory=OrganizedItems)
    unidentified_unique: OrganizedItems = Field(default_factory=OrganizedItems)

    def extend(self, categorized_items: "OrganizedItemsByCategory"):
        self.unique.extend(categorized_items.unique)
        self.unidentified_unique.extend(categorized_items.unidentified_unique)

    def is_empty(self) -> bool:
        for table_name in self.model_fields:
            table: OrganizedItems = getattr(self, table_name)
            is_empty = table.is_empty()
            if not is_empty:
                return is_empty

        return True
