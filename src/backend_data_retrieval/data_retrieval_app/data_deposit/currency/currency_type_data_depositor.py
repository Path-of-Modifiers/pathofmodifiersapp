from collections.abc import Iterator

import requests
from backend_api.app.core.schemas.currency import (
    CurrencyType,
    CurrencyTypeCreate,
    CurrencyTypeUpdate,
)
from pydantic import TypeAdapter

from data_retrieval_app.data_deposit.data_depositor_base import DataDepositorBase
from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.external.currency import (
    ExchangeRatioItem,
)
from data_retrieval_app.logs.logger import data_deposit_logger as logger
from data_retrieval_app.pom_api_authentication import get_superuser_token_headers
from data_retrieval_app.utils import get_data_safe, post_data_safe


class CurrencyTypeDataDepositor(DataDepositorBase):
    def __init__(self):
        self.base_url = settings.BACKEND_BASE_URL
        self.pom_auth_headers = get_superuser_token_headers(self.base_url)

        self.data_url = f"{self.base_url}/currency/type/"

        self.name_to_trade_name = self._get_name_to_trade_name_dict()

    def _get_name_to_trade_name_dict(self) -> dict[str, str]:
        """
        Retrieves a map for "fancy" currency names, as used in the API, to their trade names, which we need.
        """
        headers = {
            "User-Agent": f"OAuth pathofmodifiers/{settings.TAG} (contact: {settings.OATH_ACC_TOKEN_CONTACT_EMAIL}) StrictMode"
        }
        response = get_data_safe(
            "https://www.pathofexile.com/api/trade/data/static",
            headers=headers,
            logger=logger,
        )

        response_json = response.json()
        result = response_json["result"]
        currencies = dict[str, str]()
        for category in result:
            if category["id"] == "Currency":
                for entry in category["entries"]:
                    name = entry["text"]
                    trade_name = entry["id"]
                    currencies[name] = trade_name

        return currencies

    def _get_current_currency_types(self) -> list[CurrencyType]:
        response = get_data_safe(
            self.data_url,
            headers=self.pom_auth_headers,
            logger=logger,
        )

        return TypeAdapter(list[CurrencyType]).validate_python(response.json())

    def _load_data(self) -> Iterator[list[ExchangeRatioItem]]:
        response = get_data_safe(
            "https://api.poe.watch/exchange/ratios?league=Standard&game=poe1",
            logger=logger,
        )
        response_json = response.json()
        currency_items = list[ExchangeRatioItem]()
        currency_item_adaptor = TypeAdapter(ExchangeRatioItem)
        for item in response_json["items"]:
            if item["category"] == "currency":
                item["leagueId"] = -1
                currency_items.append(currency_item_adaptor.validate_python(item))

        yield currency_items

    def _process_data(
        self, currency_items: list[ExchangeRatioItem]
    ) -> list[CurrencyTypeCreate]:
        """
        Scenarios that requires updated currency:
            Name is:
                - 'TEMP_NAME': this is right after the 'ee1239y6yfda' migration,
                  as the database has no knowledge of name
                - not the same when trade name is
            Trade name is:
                - not the same when name is
            Incoming currency always takes precedence
        """
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        headers.update(self.pom_auth_headers)

        current_currencies = self._get_current_currency_types()
        processed_currencies = list[CurrencyTypeCreate]()

        found_chaos = False
        for currency in currency_items:
            trade_name = self.name_to_trade_name.get(currency.name)
            if trade_name is None:
                continue

            currency_id = -1

            found_duplicate = False
            need_update = False
            for current_currency in current_currencies:
                if (
                    current_currency.name == "TEMP_NAME"
                    and current_currency.tradeName == trade_name
                ):
                    need_update = True
                if (
                    current_currency.name == currency.name
                    and current_currency.tradeName != trade_name
                ):
                    need_update = True
                if (
                    current_currency.name != currency.name
                    and current_currency.tradeName == trade_name
                ):
                    need_update = True
                if (
                    current_currency.name == currency.name
                    and current_currency.tradeName == trade_name
                ):
                    found_duplicate = True

                if current_currency.tradeName == "chaos":
                    found_chaos = True

                if found_duplicate or need_update:
                    currency_id = current_currency.currencyId
                    break

            if need_update:
                updated_currency = CurrencyTypeUpdate(
                    currencyId=currency_id, name=currency.name, tradeName=trade_name
                )

                try:
                    response = requests.put(
                        self.data_url,
                        json=updated_currency.model_dump(),
                        headers=headers,
                    )
                    response.raise_for_status()
                except Exception as e:
                    logger.error(
                        f"The following error occurred while inserting data: {e}"
                    )
                    raise e

            elif not found_duplicate:
                processed_currencies.append(
                    CurrencyTypeCreate(name=currency.name, tradeName=trade_name)
                )

        if not found_chaos:
            processed_currencies.append(
                CurrencyTypeCreate(name="Chaos Orb", tradeName="Chaos")
            )

        return processed_currencies

    def _insert_data(self, currencies: list[CurrencyTypeCreate]):
        if not currencies:
            return

        logger.info("Inserting data into database.")
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        headers.update(self.pom_auth_headers)

        post_data_safe(
            self.data_url,
            json=TypeAdapter(list[CurrencyTypeCreate]).dump_python(currencies),
            headers=headers,
        )

        logger.info("Successfully inserted data into database.")
