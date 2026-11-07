from collections.abc import Sequence

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
    removed_items: list[CacheItemWithContext] = Field(
        default_factory=list[CacheItemWithContext]
    )
    changed_items: list[PoeItem] = Field(default_factory=list[PoeItem])
    new_items: list[PoeItem] = Field(default_factory=list[PoeItem])

    def extend(self, category: "OrganizedItems"):
        self.removed_items.extend(category.removed_items)
        self.changed_items.extend(category.changed_items)
        self.new_items.extend(category.new_items)

    def is_empty(self) -> bool:
        return not (self.removed_items or self.changed_items or self.new_items)


class OrganizedItemsByCategory(PoeModel):
    """
    Field names much match the identifiers of the category detectors
    """

    unique: OrganizedItems = Field(default_factory=OrganizedItems)
    unidentified_unique: OrganizedItems = Field(default_factory=OrganizedItems)

    def iter_categories(self) -> Sequence[OrganizedItems]:
        return [getattr(self, category_name) for category_name in self.model_fields]

    def extend(self, categorized_items: "OrganizedItemsByCategory"):
        for category, donor_category in zip(
            self.iter_categories(), categorized_items.iter_categories(), strict=True
        ):
            category.extend(donor_category)

    def is_empty(self) -> bool:
        return all(category.is_empty() for category in self.iter_categories())
