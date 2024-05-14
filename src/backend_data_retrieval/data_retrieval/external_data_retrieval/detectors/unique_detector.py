import pandas as pd

from external_data_retrieval.detectors.base import DetectorBase


class UniqueDetector(DetectorBase):
    def _specialized_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        if "rarity" not in df.columns:
            return pd.DataFrame(columns=df.columns)

        df = df.loc[df["rarity"] == "Unique"]

        df = df.loc[df["name"].isin(self.wanted_items)]

        temp_df = df["name"] + df["baseType"]
        for name_baseType in temp_df.unique():
            if not name_baseType in self.found_items:
                self.found_items[name_baseType] = True

        return df


class UniqueJewelDetector(UniqueDetector):
    wanted_items_dict = {
        "Cobalt Jewel": ["Grand Spectrum", "Forbidden Flesh", "The Balance of Terror"],
        "Crimson Jewel": [
            "That Which Was Taken",
            "Grand Spectrum",
            "Forbidden Flame",
            "Split Personality",
            "Thread of Hope",
        ],
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
        "The Balance of Terror",
        "That Which Was Taken",
        "Forbidden Flame",
        "Split Personality",
        "Thread of Hope",
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

    def __str__(self):
        return "Unique Jewel Detector"


class UniqueJewelleryDetector(UniqueDetector):
    wanted_items_dict = {
        "Onyx Amulet": ["Aul's Uprising", "Replica Dragonfang's Flight"],
        "Gold Amulet": ["The Utmost"],
        "Ruby Ring": ["Precursor's Emblem", "Circle of Anguish"],
        "Sapphire Ring": ["Precursor's Emblem", "Circle of Fear"],
        "Topaz Ring": ["Precursor's Emblem", "Circle of Regret"],
        "Prismatic Ring": ["Precursor's Emblem", "Circle of Ambition"],
        "Two-Stone Ring": ["Precursor's Emblem"],
        "Iron Ring": ["Circle of Guilt"],
        "Amethyst Ring": ["Circle of Nostalgia"],
    }
    wanted_items = [
        "Aul's Uprising",
        "Replica Dragonfang's Flight",
        "The Utmost",
        "Precursor's Emblem",
        "Circle of Ambition",
        "Circle of Guilt",
        "Circle of Anguish",
        "Circle of Regret",
        "Circle of Fear",
        "Circle of Nostalgia",
    ]

    def __str__(self):
        return "Unique Jewellery Detector"


class UniqueArmourDetector(UniqueDetector):
    wanted_items_dict = {
        "Great Crown": ["Forbidden Shako"],
        "Simple Robe": ["Skin of the Lords"],
        "Carnal Armour": ["Shroud of the Lightless"],
    }
    wanted_items = ["Forbidden Shako", "Skin of the Lords", "Shroud of the Lightless"]

    def __str__(self):
        return "Unique Armour Detector"


class UniqueWeaponDetector(UniqueDetector):
    wanted_items_dict = {"Vaal Rapier": ["Paradoxica"]}
    wanted_items = ["Paradoxica"]

    def __str__(self):
        return "Unique Weapon Detector"
