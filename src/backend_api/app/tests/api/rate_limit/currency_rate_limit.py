from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.base_test import BaseTest
from app.tests.types import ObjectGeneratorFunc


@pytest.mark.usefixtures("clear_db", autouse=True)
class TestCurrencyRateLimit(BaseTest):
    @pytest.mark.anyio
    async def test_get_currency_rate_limit(
        self,
        db: Session,
        normal_user_token_headers: dict[str, str],
        async_client: AsyncClient,
        unique_identifier: str,
        route_prefix: str,
        object_generator_func: ObjectGeneratorFunc,
    ) -> None:
        _, object_out = await self._create_random_object_crud(db, object_generator_func)

        obj_out_pk_map = self._create_primary_key_map(object_out)
        print("RATE LIMIT BEFORE PATCH", settings.RATE_LIMIT)
        with patch(
            "app.core.config.settings.RATE_LIMIT",
            True,
        ):
            print(type(settings.RATE_LIMIT))
            print("RATE LIMIT AFTER PATCH", settings.RATE_LIMIT)
            for _ in range(8):
                response = await async_client.get(
                    f"{settings.API_V1_STR}/{route_prefix}/{obj_out_pk_map[unique_identifier]}",
                    headers=normal_user_token_headers,
                )
            print("RESPONSE DDDDD", response.json())
            # print(response.headers["Retry-After-Seconds"])
            assert response.status_code == 429

    # @pytest.mark.anyio
    # async def test_get_latest_currency_id_rate_limit(
    #     self, async_client: AsyncClient, normal_user_token_headers: dict[str, str]
    # ) -> None:
    #     pass
