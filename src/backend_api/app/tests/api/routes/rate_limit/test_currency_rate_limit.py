from unittest.mock import patch

import pytest
from sqlalchemy.orm import Session

from app.tests.base_test import BaseTest
from app.tests.types import AsyncFunction, ObjectGeneratorFunc


@pytest.mark.usefixtures("clear_db", autouse=True)
@pytest.mark.usefixtures("clear_cache", autouse=True)
class TestCurrencyRateLimit(BaseTest):
    @pytest.mark.anyio
    async def test_get_currency_rate_limit(
        self,
        db: Session,
        get_object_from_api: AsyncFunction,
        object_generator_func: ObjectGeneratorFunc,
    ) -> None:
        _, object_out = await self._create_random_object_crud(db, object_generator_func)

        obj_out_pk_map = self._create_primary_key_map(object_out)
        print("ojanfdasfiusfd", get_object_from_api.__code__.co_varnames)
        with patch(
            "app.core.config.settings.RATE_LIMIT",
            "True",
        ):
            for _ in range(5):
                response = await get_object_from_api(obj_out_pk_map)
            print("djoasjfdaoifj", response.json()["detail"])
            raise Exception
            print(response.headers["Retry-After-Seconds"])
            assert response.status_code == 429

    # @pytest.mark.anyio
    # async def test_get_latest_currency_id_rate_limit(
    #     self, async_client: AsyncClient, normal_user_token_headers: dict[str, str]
    # ) -> None:
    #     pass
