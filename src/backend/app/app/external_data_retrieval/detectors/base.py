class DetectorBase:
    """
    Base class for searching stashes for items we want to store and process further
    """

    wanted_items = {}
    found_items = {}

    def __init__(self) -> None:
        """
        `self.n_unique_items_found` needs to be stored inbetween item detector sessions.
        """
        self.n_unique_items_found = 0

    def iterate_stashes(self, stashes: list) -> tuple:
        """
        Goes through all stashes searching for items that correspond to `self.wanted_items`.
        `self.n_unique_items_found` is calculated by the number of keys in `self.found_items`.
        The `_check_item` method, which is unique to item categories, is defined in a child class.

        Parameters:
            :param stashes: (list) A list of stash objects as defined by GGG.
            :return: (tuple) Wanted stashes, how many new items was found, number of different items that have been found so far, stashes that still need to be filtered.
        """
        item_count = 0

        # Lists of stashes to be populated
        wanted_stashes = []
        leftover_stashes = []
        for stash in stashes:
            if (
                stash["public"] and stash["items"]
            ):  # Checks if the stash is public and contains items
                # Lists of items
                stash_wanted_items = []
                stash_leftover_items = []
                for item in stash["items"]:
                    if self._check_item(item):  # Checks if we want the item
                        stash_wanted_items.append(item)
                        item_count += 1
                    else:
                        stash_leftover_items.append(item)

                # Replaces only the `items` object in stashes
                stash["items"] = stash_leftover_items
                leftover_stashes.append(stash)

                # Only adds stashes to `wanted_stashes` if items were found
                if stash_wanted_items:
                    stash["items"] = stash_wanted_items
                    wanted_stashes.append(stash)

        self.n_unique_items_found = len(self.found_items.keys())
        return wanted_stashes, item_count, self.n_unique_items_found, leftover_stashes
