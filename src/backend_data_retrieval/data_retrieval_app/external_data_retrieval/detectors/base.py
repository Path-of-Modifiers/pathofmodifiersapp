from abc import ABC, abstractmethod

from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.external.poe import (
    PoeItem,
    Stash,
)


class SubCategoryDetectorBase(ABC):
    wanted_items: list[str]

    def is_wanted(self, item: PoeItem) -> bool:
        return item.name in self.wanted_items

    @abstractmethod
    def __str__(self):
        """Returns a descriptive name for the sub category"""


class CategoryDetectorBase(ABC):
    """
    Base class for searching stashes for items we want to store and process further
    """

    identifier: str

    should_cache: bool

    detectors: list[SubCategoryDetectorBase]

    @abstractmethod
    def matches_category(self, item: PoeItem) -> bool:
        """Returns true or false based on the criteria of the detector"""

    def find_interesting_items(
        self, donor_stash: Stash, receiver_stash: Stash, no_cache_receiver_stash: Stash
    ):
        donated_items = list[str]()
        for i, item in enumerate(donor_stash.items):
            if not self.matches_category(item):
                continue

            is_wanted = False
            for detector in self.detectors:
                is_wanted = detector.is_wanted(item)
                if is_wanted:
                    break

            if is_wanted:
                if self.should_cache:
                    receiver_stash.items.append(item)
                else:
                    no_cache_receiver_stash.items.append(item)
                donated_items.append(i)

        for idx in reversed(donated_items):
            donor_stash.items.pop(idx)
