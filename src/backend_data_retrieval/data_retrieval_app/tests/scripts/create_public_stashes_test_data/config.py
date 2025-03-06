from pydantic_settings import BaseSettings


class PoEPublicStashesTestDataSettings(BaseSettings):
    N_OF_ITEMS_PER_MODIFIER_FILE: int = 10
    MODIFIER_CATEGORIES_TO_ITERATE: list[str] = []  # For instance ["unique", "idol"]
    MODIFIER_CSV_FILES_TO_ITERATE: list[
        str
    ] = []  # For instance: ["unique/AulsUprising.csv", "unique/ThreadOfHope.csv"] (overrides categories)

    MINI_BATCH_SIZE: int = 10
    N_CHECKPOINTS_PER_TRANSFORMATION: int = 1

    CREATE_TEST_DATA_FOR_N_SECONDS: int = 10 * 60  # 10 min
    CREATE_DATA_DIFFERENT_TIMING_INTERVAL: bool = (
        True  # Provides variety to timing of data created
    )
    TIMING_PERIOD: int = 10  # Amount of days the data gets dispersed when created. Maximum days up to equivalent <10 years.

    @property
    def dispersed_timing_enabled(self) -> bool:
        return bool(self.CREATE_DATA_DIFFERENT_TIMING_INTERVAL and self.TIMING_PERIOD)

    ITEM_NOTE_CURRENCY_TYPES: list[str] = [
        "chaos",
    ]  # , "divine", "mirror", etc.
    MEAN_ITEM_PRICE: int = 200


script_settings = PoEPublicStashesTestDataSettings()
