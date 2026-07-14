import pandas as pd

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.logs.logger import transform_logger as logger
from data_retrieval_app.pom_api_authentication import get_superuser_token_headers
from data_retrieval_app.utils import get_data_safe, insert_data


class TransformCurrencyAPIData:
    def __init__(self) -> None:
        logger.debug("Initializing TransformCurrencyAPIData.")
        self.base_url = settings.BACKEND_BASE_URL
        logger.debug(f"Url set to: {self.base_url}")
        self.pom_api_headers = get_superuser_token_headers(self.base_url)
        logger.debug("Headers set to: " + str(self.pom_api_headers))
        logger.debug("Initializing TransformCurrencyAPIData done.")

        self.name_to_trade_name = self._get_name_to_trade_name_dict()

    def _get_name_to_trade_name_dict(self) -> dict:
        """
        Retrieves a map for "fancy" currency names, as used in the API, to their trade names, which we need.
        """
        headers = {
            "User-Agent": f"OAuth pathofmodifiers/0.1.0 (contact: {settings.OATH_ACC_TOKEN_CONTACT_EMAIL}) StrictMode"
        }
        response = get_data_safe(
            "https://www.pathofexile.com/api/trade/data/static",
            headers=headers,
            logger=logger,
        )

        response_json = response.json()
        result = response_json["result"]
        currencies = {}
        for category in result:
            if category["id"] == "Currency":
                for entry in category["entries"]:
                    name = entry["text"]
                    trade_name = entry["id"]
                    currencies[name] = trade_name

        return currencies

    def _transform_currency_table(
        self, currency_df: pd.DataFrame, current_hours: dict[int, int]
    ) -> pd.DataFrame:
        """
        Since a chaos orb is always worth one chaos orb, ninja does not include it in its price api.
        """

        missing_chaos_value_mask = (currency_df["chaos.chaosValue"] == 0) | (
            currency_df["chaos.chaosValue"].isna()
        )
        currency_df["chaos.chaosValue"] = currency_df["chaos.chaosValue"].where(
            ~missing_chaos_value_mask,
            currency_df["divine.chaosValue"],
        )

        chaos_dict = {
            "name": ["Chaos Orb"],
            "chaos.chaosValue": [1],
        }
        for league_id in currency_df["leagueId"].unique():
            chaos_dict["leagueId"] = [league_id]
            chaos_df = pd.DataFrame.from_dict(chaos_dict)
            currency_df = pd.concat((currency_df, chaos_df), ignore_index=True)

        currency_df["tradeName"] = currency_df["name"].map(
            lambda name: self.name_to_trade_name.get(name, pd.NA)
        )

        currency_df["createdHoursSinceLaunch"] = currency_df["leagueId"].map(
            current_hours
        )
        return currency_df

    def _clean_currency_table(self, currency_df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans the currency table of unnecessary columns.
        """
        currency_df = currency_df.rename(columns={"chaos.chaosValue": "valueInChaos"})

        currency_df = currency_df.drop(
            currency_df.columns.difference(
                ["tradeName", "valueInChaos", "createdHoursSinceLaunch", "leagueId"]
            ),
            axis=1,
        )
        currency_df = currency_df.loc[~currency_df["tradeName"].isna()].reset_index(
            drop=True
        )
        return currency_df

    def _get_latest_currency_id_series(self, currency_df: pd.DataFrame) -> pd.Series:
        response = get_data_safe(
            f"{self.base_url}/currency/latest_currency_id/",
            headers=self.pom_api_headers,
            logger=logger,
        )
        latest_currency_id = int(response.text)

        currency_id = pd.Series(
            range(latest_currency_id - len(currency_df) + 1, latest_currency_id + 1),
            dtype=int,
        )
        return currency_id

    def transform_into_tables(
        self, currency_df: pd.DataFrame, current_hours: dict[int, int]
    ) -> pd.DataFrame:
        """
        Transforms the data into tables and transforms with help functions.
        """
        logger.debug("Transforming data into tables.")
        currency_df = self._transform_currency_table(currency_df, current_hours)
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
