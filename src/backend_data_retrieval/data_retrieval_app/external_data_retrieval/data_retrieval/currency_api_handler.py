from collections.abc import Sequence

from backend_api.app.core.schemas.currency import Currency, CurrencyType
from backend_api.app.core.schemas.league import League
from pydantic import TypeAdapter

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.external.currency import (
    ExchangeRatioItem,
)
from data_retrieval_app.external_data_retrieval.transforming_data.transform_currency_api_data import (
    TransformCurrencyAPIData,
)
from data_retrieval_app.logs.logger import external_data_retrieval_logger as logger
from data_retrieval_app.pom_api_authentication import (
    get_superuser_token_headers,
)
from data_retrieval_app.utils import send_request_safe


class CurrencyAPIHandler:
    backend_base_url = settings.BACKEND_BASE_URL
    pom_auth_headers = get_superuser_token_headers(backend_base_url)

    currency_url = f"{backend_base_url}/currency/"

    def __init__(self, url: str) -> None:
        self.url = url

        self.currency_item_adapter = TypeAdapter(ExchangeRatioItem)

        self.currency_types = self._get_currency_types()
        self.transformer = TransformCurrencyAPIData(self.currency_types)

    def _get_currency_types(self) -> dict[str, CurrencyType]:
        response = send_request_safe(
            "get",
            self.currency_url + "type/",
            headers=self.pom_auth_headers,
            logger=logger,
        )

        currency_types = TypeAdapter(list[CurrencyType]).validate_python(
            response.json()
        )
        return {currency_type.name: currency_type for currency_type in currency_types}

    def _get_latest_currencies(
        self, leagues: Sequence[League]
    ) -> dict[tuple[int, str], Currency]:
        response = send_request_safe(
            "get",
            self.currency_url + "price/latest/",
            params={"league_ids": [league.leagueId for league in leagues]},
            headers=self.pom_auth_headers,
            logger=logger,
        )
        currency_list = TypeAdapter(list[Currency]).validate_python(response.json())

        currencies = dict[tuple[int, str], Currency]()
        for currency in currency_list:
            currencies[(currency.leagueId, currency.tradeName)] = currency

        return currencies

    def _remove_old_currencies(
        self,
        currencies: dict[tuple[int, str], Currency],
        leagues: list[League],
        current_hours: dict[int, int],
    ) -> list[League]:
        """
        Modifies latest currencies inplace
        """
        if not currencies:
            # No prior data is available
            return leagues

        leagues_needs_new_data = set[int]()
        for (league_id, _), currency in currencies.items():
            current_hour = current_hours[league_id]
            currency_hour = currency.createdHoursSinceLaunch
            if currency_hour != current_hour:
                leagues_needs_new_data.add(league_id)

        return [
            league for league in leagues if league.leagueId in leagues_needs_new_data
        ]

    def _get_new_data(self, leagues: list[League]) -> list[ExchangeRatioItem]:
        currency_items = list[ExchangeRatioItem]()
        for league in leagues:
            response = send_request_safe(
                "get",
                self.url.format(league=league.name.replace(" ", "+")),
                logger=logger,
            )
            response_json = response.json()

            for item in response_json["items"]:
                if item["category"] == "currency":
                    item["leagueId"] = league.leagueId
                    currency_items.append(
                        self.currency_item_adapter.validate_python(item)
                    )

        return currency_items

    def get_currency_data(
        self, leagues: list[League], current_hours: dict[int, int]
    ) -> dict[tuple[int, str], Currency]:
        """
        Returns a dict mapping trade name to list of the same currency per league
        """
        currencies = self._get_latest_currencies(leagues)

        leagues_needs_new_data = self._remove_old_currencies(
            currencies, leagues, current_hours
        )

        if leagues_needs_new_data:
            exchange_ratios = self._get_new_data(leagues_needs_new_data)
            currencies.update(
                self.transformer.transform_and_insert(exchange_ratios, current_hours)
            )

        return currencies

    def store_data_to_csv(self, path: str) -> None:
        """
        Stores the data in a CSV. Only to be used for testing purposes.
        """
        # currencies_df = self.make_request()

        # currencies_df.to_csv(path + "/currencies.csv", index=False)
        raise NotImplementedError()
