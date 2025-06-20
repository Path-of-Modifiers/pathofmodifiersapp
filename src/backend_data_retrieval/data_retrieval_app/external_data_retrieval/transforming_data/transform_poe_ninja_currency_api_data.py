import pandas as pd
import requests

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.external_data_retrieval.data_retrieval.poe_ninja_currency_api_handler import (
    PoENinjaCurrencyAPIHandler,
)
from data_retrieval_app.logs.logger import transform_logger as logger
from data_retrieval_app.pom_api_authentication import get_superuser_token_headers
from data_retrieval_app.utils import find_hours_since_launch, insert_data


def load_currency_data():
    """
    Loads data from the poe.ninja currency API.
    """
    poe_ninja_currency_api_handler = PoENinjaCurrencyAPIHandler(
        url=f"https://poe.ninja/api/data/currencyoverview?league={settings.CURRENT_SOFTCORE_LEAGUE}&type=Currency"
    )

    currencies_df = poe_ninja_currency_api_handler.make_request()

    return currencies_df


class TransformPoENinjaCurrencyAPIData:
    def __init__(self) -> None:
        logger.debug("Initializing TransformPoENinjaCurrencyAPIData.")
        self.base_url = settings.BACKEND_BASE_URL
        logger.debug(f"Url set to: {self.base_url}")
        self.pom_api_headers = get_superuser_token_headers(self.base_url)
        logger.debug("Headers set to: " + str(self.pom_api_headers))
        logger.debug("Initializing TransformPoENinjaCurrencyAPIData done.")

    def _create_currency_table(self, currency_df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates the currency table.
        """
        currency_df.rename(
            columns={
                "tradeId": "tradeName",
                "chaosEquivalent": "valueInChaos",
            },
            inplace=True,
        )
        return currency_df

    def _transform_currency_table(
        self, currency_df: pd.DataFrame, hours_since_launch: int
    ) -> pd.DataFrame:
        """
        Since a chaos orb is always worth one chaos orb, ninja does not include it in its price api.
        """
        chaos_dict = {
            "tradeName": ["chaos"],
            "valueInChaos": [1],
        }
        chaos_df = pd.DataFrame.from_dict(chaos_dict)
        currency_df = pd.concat((currency_df, chaos_df), ignore_index=True)

        currency_df["createdHoursSinceLaunch"] = hours_since_launch
        return currency_df

    def _clean_currency_table(self, currency_df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans the currency table of unnecessary columns.
        """

        currency_df.drop(
            currency_df.columns.difference(
                ["tradeName", "valueInChaos", "createdHoursSinceLaunch"]
            ),
            axis=1,
            inplace=True,
        )
        currency_df = currency_df.loc[~currency_df["tradeName"].isna()].reset_index()
        return currency_df

    def _get_latest_currency_id_series(self, currency_df: pd.DataFrame) -> pd.Series:
        try:
            response = requests.get(
                f"{self.base_url}/currency/latest_currency_id/",
                headers=self.pom_api_headers,
            )
            response.raise_for_status()
        except Exception as e:
            logger.error(
                f"The following error occurred while making request _get_latest_currency_id_series: {e}"
            )
            raise e
        latest_currency_id = int(response.text)

        currency_id = pd.Series(
            range(latest_currency_id - len(currency_df) + 1, latest_currency_id + 1),
            dtype=int,
        )
        return currency_id

    def transform_into_tables(self, currency_df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the data into tables and transforms with help functions.
        """
        hours_since_launch = find_hours_since_launch()
        logger.debug("Transforming data into tables.")
        currency_df = self._create_currency_table(currency_df)
        currency_df = self._transform_currency_table(currency_df, hours_since_launch)
        logger.debug("Successfully transformed data into tables.")

        logger.debug("Cleaning currency table data.")
        currency_df = self._clean_currency_table(currency_df)
        logger.debug("Successfully cleaned currency table data.")

        logger.debug("Inserting currency data into database.")
        insert_data(
            currency_df,
            url=self.base_url,
            table_name="currency",
            logger=logger,
            headers=self.pom_api_headers,
        )
        logger.debug("Successfully inserted currency data into database.")

        currency_id = self._get_latest_currency_id_series(currency_df)
        logger.debug("Latest currency id found: " + str(currency_id))

        currency_df = currency_df.assign(currencyId=currency_id)
        logger.debug("Successfully transformed data into tables.")
        return currency_df
