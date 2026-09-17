from abc import ABC, abstractmethod

from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.poe_schema import (
    Item,
    Stash,
)


class DetectorBase(ABC):
    """
    Base class for searching stashes for items we want to store and process further
    """

    should_cache: bool
    wanted_items: list[str]

    @abstractmethod
    def _is_wanted(self, item: Item) -> bool:
        """Returns true or false based on the criteria of the detector"""

    def find_interesting_items(
        self, donor_stash: Stash, receiver_stash: Stash, no_cache_receiver_stash: Stash
    ):
        donated_items = list[str]()
        for i, item in enumerate(donor_stash.items):
            if not self._is_wanted(item):
                continue

            if self.should_cache:
                receiver_stash.items.append(item)
            else:
                no_cache_receiver_stash.items.append(item)
            donated_items.append(i)

        for idx in reversed(donated_items):
            donor_stash.items.pop(idx)
