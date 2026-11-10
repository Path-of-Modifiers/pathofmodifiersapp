import random

from data_retrieval_app.external_data_retrieval.detectors.unique_detector import (
    UnidentifiedUniqueDetector,
    UniqueDetector,
)


def get_icons() -> dict[str, str]:
    name_by_icon = UnidentifiedUniqueDetector.wanted_item_icons

    icon_by_name = dict[str, str]()
    for icon, name in name_by_icon.items():
        icon_by_name[name] = icon

    return icon_by_name


def get_wanted_item(detector: UniqueDetector, *, rng: random.Random = None) -> str:
    if rng is None:
        rng = random.Random()

    sub_category_detector = rng.choice(detector.detectors)
    wanted_item = rng.choice(sub_category_detector.wanted_items)
    return wanted_item
