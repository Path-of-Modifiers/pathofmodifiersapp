from app.external_data_retrieval.detectors.base import DetectorBase


class UniqueDetector(DetectorBase):
    def _check_item(self, item: dict) -> bool:
        if (
            item["baseType"] in self.wanted_items
        ):  # Checks if the unique is a basetyp we are interested in
            if (
                item["name"] in self.wanted_items[item["baseType"]]
            ):  # Check if the unique is one that we want
                # Records the item as found, which is used to count number of unique items found
                self.found_items[item["name"] + " " + item["baseType"]] = True
                return True
        return False


class UniqueJewelDetector(UniqueDetector):
    """
    Contains only a dictionary of wanted uniques and with their basetype as
    """

    wanted_items = {
        "Cobalt Jewel": ["Grand Spectrum", "Forbidden Flesh"],
        "Crimson Jewel": ["That Which Was Taken", "Grand Spectrum", "Forbidden Flame"],
        "Viridian Jewel": ["Impossible Escape", "Grand Spectrum"],
        "Prismatic Jewel": ["Watcher's Eye", "Sublime Vision"],
        "Timeless Jewel": [
            "Glorious Vanity",
            "Lethal Pride",
            "Brutal Restraint",
            "Militant Faith",
            "Elegant Hubris",
        ],
        "Large Cluster Jewel": ["Voices"],
    }
