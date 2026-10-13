from collections.abc import Iterator

from backend_api.app.core.schemas.currency import (
    Currency,
    CurrencyPriceCreate,
    CurrencyType,
)
from pydantic import TypeAdapter

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.external.currency import (
    ExchangeRatioItem,
)
from data_retrieval_app.logs.logger import transform_logger as logger
from data_retrieval_app.pom_api_authentication import get_superuser_token_headers
from data_retrieval_app.utils import send_request_safe


class TransformCurrencyAPIData:
    def __init__(self, name_to_currency: dict[str, CurrencyType]) -> None:
        logger.debug("Initializing TransformCurrencyAPIData.")
        self.base_url = settings.BACKEND_BASE_URL
        self.url = f"{self.base_url}/currency/price/"
        logger.debug(f"Url set to: {self.url}")
        self.pom_api_headers = get_superuser_token_headers(self.base_url)
        logger.debug("Headers set to: " + str(self.pom_api_headers))
        logger.debug("Initializing TransformCurrencyAPIData done.")

        self.name_to_currency = name_to_currency

    def _transform(
        self,
        exchange_ratios: list[ExchangeRatioItem],
        current_hours: dict[int, int],
    ) -> dict[tuple[int, str], Currency]:
        """
        Since a chaos orb is always worth one chaos orb, ninja does not include it in its price api.
        """
        currencies = dict[tuple[int, str], Currency]()
        for ratio in exchange_ratios:
            currency_type = self.name_to_currency.get(ratio.name)
            if currency_type is None:
                continue

            value = -1
            if ratio.chaos.chaosValue is None or ratio.chaos.chaosValue == 0:
                value = ratio.divine.chaosValue
            else:
                value = ratio.chaos.chaosValue

            current_hour = current_hours[ratio.leagueId]
            currency_id = currency_type.currencyId
            trade_name = currency_type.tradeName

            currency = Currency(
                currencyId=currency_id,
                tradeName=trade_name,
                name=ratio.name,
                leagueId=ratio.leagueId,
                createdHoursSinceLaunch=current_hour,
                valueInChaos=value,
            )

            currencies[currency.leagueId, currency.tradeName] = currency

        for league_id, current_hour in current_hours.items():
            name = "Chaos Orb"
            currency_type = self.name_to_currency[name]
            currency_id = currency_type.currencyId
            trade_name = currency_type.tradeName
            chaos_currency = Currency(
                currencyId=currency_id,
                tradeName=trade_name,
                name=name,
                leagueId=league_id,
                createdHoursSinceLaunch=current_hour,
                valueInChaos=1,
            )
            currencies[
                chaos_currency.leagueId, chaos_currency.tradeName
            ] = chaos_currency

        return currencies

    def _insert(self, currencies: Iterator[Currency]):
        prices = list[CurrencyPriceCreate]()
        for currency in currencies:
            prices.append(
                CurrencyPriceCreate(
                    currencyId=currency.currencyId,
                    leagueId=currency.leagueId,
                    createdHoursSinceLaunch=currency.createdHoursSinceLaunch,
                    valueInChaos=currency.valueInChaos,
                )
            )

        headers = {"accept": "application/json", "Content-Type": "application/json"}
        headers.update(self.pom_api_headers)
        send_request_safe(
            "post",
            self.url,
            json=TypeAdapter(list[CurrencyPriceCreate]).dump_python(prices),
            headers=headers,
        )

    def transform_and_insert(
        self, exchange_ratios: list[ExchangeRatioItem], current_hours: dict[int, int]
    ) -> dict[tuple[int, str], Currency]:
        logger.debug("Transforming exchange ratios into currencies.")
        currencies = self._transform(exchange_ratios, current_hours)
        logger.debug("Inserting currency prices.")
        self._insert(currencies.values())
        logger.debug("Successfully inserted currency data into database.")

        return currencies
