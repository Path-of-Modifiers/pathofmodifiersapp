import pandas as pd

from data_retrieval_app.external_data_retrieval.detectors.base import DetectorBase
from data_retrieval_app.logs.logger import main_logger as logger


class UniqueDetector(DetectorBase):
    def _check_if_wanted(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.loc[df["name"].isin(self.wanted_items)]
        return df

    def _specialized_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        if "rarity" not in df.columns:
            return pd.DataFrame(columns=df.columns)

        df = df.loc[df["rarity"] == "Unique"]

        df = self._check_if_wanted(df)

        if self.pbar_enabled:
            temp_df = df["name"] + df["baseType"]
            for name_baseType in temp_df.unique():
                if name_baseType not in self.found_items:
                    self.found_items[name_baseType] = True

        return df


class UniqueFoulbornDetector(UniqueDetector):
    def _check_if_wanted(self, df: pd.DataFrame) -> pd.DataFrame:
        if "mutated" not in df.columns:
            logger.error("MUTATED NOT IN")
            return pd.DataFrame(columns=df.columns)

        df_filtered = df[df["mutated"].astype(str) == "True"].loc[
            df["name"].str.len() != 0
        ]

        return df_filtered

    def __str__(self):
        return "Unique Foulborn Detector"


class UniqueUnidentifiedDetector(UniqueDetector):
    """
    Notes:
    Precursor's Emblems, Shroud of the Lightless and Paradoxica are not supported.
    Why:
        Prcursor's Emblems: Too many variation per item base. Multiple icons per base,
                            and I am assuming the icon is related to which items were used
                            to create the item, which would in return influence the price.
        Shroud of the Lightless and Paradoxica: They have replica counterparts which can't
                                                be distinguished.

    Is this a problem?
        No, because they are not particularly sought after in their un-id form
    """

    wanted_base_types = [
        "Viridian Jewel",
        "Cobalt Jewel",
        "Crimson Jewel",
        "Prismatic Jewel",
        "Timeless Jewel",
        "Large Cluster Jewel",
        "Onyx Amulet",
        "Gold Amulet",
        "Ruby Ring",
        "Sapphire Ring",
        "Topaz Ring",
        "Prismatic Ring",
        "Iron Ring",
        "Amethyst Ring",
        "Great Crown",
        "Simple Robe",
    ]

    wanted_item_icons = {
        "GrandSpectrum2_Green.png": "Grand Spectrum",
        "BlueGrandSpectrum.png": "Grand Spectrum",
        "RedGrandSpectrum.png": "Grand Spectrum",
        "PuzzlePieceJewel_CleansingFire.png": "Forbidden Flame",
        "PuzzlePieceJewel_GreatTangle.png": "Forbidden Flesh",
        "unique19.png": "The Balance of Terror",
        "UniqueJewelBase1.png": "Split Personality",
        "ConnectedJewel.png": "Thread of Hope",
        "TrialmasterJew.png": "The Adorned",
        "MindborePearl.png": "Impossible Escape",
        "ElderJewel.png": "Watcher's Eye",
        "SublimeVision.png": "Sublime Vision",
        "AfflictionJewel.png": "The Light of Meaning",
        "BoundByDestiny.png": "Bound By Destiny",
        "VaalCivilization.png": "Glorious Vanity",
        "KaruiCivilization.png": "Lethal Pride",
        "TemplarCivilization.png": "Militant Faith",
        "EternalEmpireCivilization.png": "Elegant Hubris",
        "UniqueJewelBase3.png": "Voices",
        "Ahn%20Artifact.png": "Aul's Uprising",
        "Malachai%27s%20BrillianceAmulet.png": "Replica Dragonfang's Flight",
        "PinnacleAmulet.png": "The Utmost",
        "UberCircleHerald.png": "Circle of Ambition",
        "SynthesisPhysical2.png": "Circle of Guilt",
        "SynthesisFire.png": "Circle of Anguish",
        "SynthesisLightning.png": "Circle of Regret",
        "SynthesisCold.png": "Circle of Fear",
        "SynthesisPhysical.png": "Circle of Nostalgia",
        "TheEpiphany.png": "Forbidden Shako",
        "MyriadGraspGrand.png": "Skin of the Lords",
    }

    def _check_if_wanted(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Uses the icon to identify which unique it is, then saving that name.
        If the name attribute still has a length of 0 it means no matching unique
        was found.
        """
        df = df.loc[(~df["identified"] & df["baseType"].isin(self.wanted_base_types))]

        for icon, name in self.wanted_item_icons.items():
            df.loc[df["icon"].str.endswith(icon), "name"] = name

        df = df.loc[df["name"].str.len() != 0]
        # self._snapshot(df)
        return df

    def __str__(self):
        return "Unidentifed Unique detector"


class UniqueJewelDetector(UniqueDetector):
    wanted_items = [
        "Grand Spectrum",
        "Forbidden Flesh",
        "Forbidden Flame",
        "The Balance of Terror",
        "That Which Was Taken",
        "Split Personality",
        "Thread of Hope",
        "The Adorned",
        "Impossible Escape",
        "Watcher's Eye",
        "Bound By Destiny",
        "Sublime Vision",
        "The Light of Meaning",
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
    wanted_items = ["Forbidden Shako", "Skin of the Lords", "Shroud of the Lightless"]

    def __str__(self):
        return "Unique Armour Detector"


class UniqueWeaponDetector(UniqueDetector):
    wanted_items = ["Paradoxica", "Cane of Kulemak"]

    def __str__(self):
        return "Unique Weapon Detector"
