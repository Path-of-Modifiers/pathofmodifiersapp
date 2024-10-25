from pydantic_settings import BaseSettings


class PoEPublicStashesTestDataSettings(BaseSettings):
    N_OF_ITEMS_PER_MODIFIER_FILE: int = 50
    MODIFIER_CSV_FILES_TO_ITERATE: list[str] = [
        "AulsUprising.csv"
    ]  # For instance: ["AulsUprising.csv", "ThreadOfHope.csv"]

    CREATE_DATA_DIFFERENT_TIMING_INTERVAL: bool = (
        True  # Provides variety to timing of data created
    )
    DAYS_AMOUNT_TIMING_INTERVAL: int = (
        20  # Amount of days the data gets dispersed when created. Maximum days up to equivalent <10 years.
    )

    @property
    def dispersed_timing_enabled(self) -> bool:
        return bool(
            self.CREATE_DATA_DIFFERENT_TIMING_INTERVAL
            and self.DAYS_AMOUNT_TIMING_INTERVAL
        )


script_settings = PoEPublicStashesTestDataSettings()
