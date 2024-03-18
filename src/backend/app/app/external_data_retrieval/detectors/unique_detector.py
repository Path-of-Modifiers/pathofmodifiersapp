import pandas as pd

from app.external_data_retrieval.detectors.base import DetectorBase


class UniqueDetector(DetectorBase):
    def _specialized_filter(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.loc[df["rarity"] == "Unique"]

        df = df.loc[df["name"].isin(self.wanted_items)]

        temp_df = df["name"] + df["baseType"]
        for name_baseType in temp_df.unique():
            if not name_baseType in self.found_items:
                self.found_items[name_baseType] = True

        return df


class UniqueJewelDetector(UniqueDetector):
    wanted_items_dict = {
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
    wanted_items = [
        "Grand Spectrum",
        "Forbidden Flesh",
        "That Which Was Taken",
        "Forbidden Flame",
        "Impossible Escape",
        "Watcher's Eye",
        "Sublime Vision",
        "Glorious Vanity",
        "Lethal Pride",
        "Brutal Restraint",
        "Militant Faith",
        "Elegant Hubris",
        "Voices",
    ]
