from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.external.poe import (
    Item,
)
from data_retrieval_app.external_data_retrieval.detectors.base import DetectorBase


class UniqueDetector(DetectorBase):
    should_cache = True

    def _is_wanted(self, item: Item) -> bool:
        if item.rarity is None or item.rarity != "Unique":
            return False
        if item.name not in self.wanted_items:
            return False

        return True


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

    should_cache = False

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
        "Leather Belt",
        "Heavy Belt",
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
        "ExpeditonCivilization.png": "Heroic Tragedy",
        "Soulcord.png": "Screams of the Desiccated",
    }

    def _is_wanted(self, item: Item) -> bool:
        """
        Uses the icon to identify which unique it is, then saving that name inplace.
        """
        if item.identified:
            return False
        if item.base_type not in self.wanted_base_types:
            return False

        icon = item.icon.split("/")[-1]
        name = self.wanted_item_icons.get(icon)
        if name is None:
            return False

        item.name = name
        return True

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
        "Heroic Tragedy",
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
        "Screams of the Desiccated",
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
