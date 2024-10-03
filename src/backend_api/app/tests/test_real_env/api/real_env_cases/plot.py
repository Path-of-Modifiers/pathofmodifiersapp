import asyncio
import time
from json import JSONDecodeError
from typing import Any

from app.logs.logger import test_logger as logger
from app.tests.test_real_env.api.real_env_base import RealEnvBase


class TestPlotRealEnv(RealEnvBase):
    def __init__(self, plot_data: dict) -> None:
        super().__init__()

        self.plot_data = plot_data
        self.plot_request_timeout = 50

        self.plot_url = self.api_v1_str + "/plot/"
        self.bulk_insert_user_url = (
            self.api_v1_str + "/test/bulk-insert-users-and-verify"
        )

    async def _async_post_plot_request(
        self, headers: dict[str, str]
    ) -> tuple[int, Any | str | None]:
        """Loop through each header and send the POST request"""
        async with self._get_async_client() as c:
            response = await c.post(
                self.plot_url,
                headers=headers,
                timeout=self.plot_request_timeout,
                json=self.plot_data,
            )
        try:
            return response.status_code, response.json()
        except JSONDecodeError:
            return response.status_code, "Invalid JSON response"

    async def perform_concurrent_plot_request(self, count: int) -> None:
        """Gets user headers and performs concurrent plotting"""
        params = {"count": count}
        # Create/get users and verify them. Retrieve headers
        super_user_headers = await self._get_superuser_token_headers()
        async with self._get_async_client() as c:
            response = await c.post(
                self.bulk_insert_user_url,
                headers=super_user_headers,
                params=params,
            )
            headers_list = response.json()
            logger.debug(f"Headers list: {headers_list}")
        headers_list = [
            {
                "Authorization": f"Bearer {header}",
                "Content-Type": "application/json",
            }
            for header in headers_list
        ]
        # Perform plotting with the user headers
        tasks = [self._async_post_plot_request(headers) for headers in headers_list]
        t = time.perf_counter()
        responses = await asyncio.gather(*tasks)
        logger.debug("Responses: " + str(responses))
        total_time = time.perf_counter() - t
        logger.info(f"Total time spent on plotting: {total_time}")


if __name__ == "__main__":
    """Playground for testing"""

    plot_data = {
        "league": "Settlers",
        "itemSpecifications": {},
        "wantedModifiers": [
            {"modifierId": 18, "position": 0, "modifierLimitations": {}}
        ],
    }
    test_plot_real_env = TestPlotRealEnv(plot_data)
    asyncio.run(test_plot_real_env.perform_concurrent_plot_request(30))
