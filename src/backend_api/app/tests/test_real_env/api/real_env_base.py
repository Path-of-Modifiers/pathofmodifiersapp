from collections.abc import AsyncGenerator

from httpx import AsyncClient

from app.core.config import settings
from app.logs.logger import setup_logging
from app.logs.logger import test_logger as logger
from app.main import app
from app.tests.utils.utils import get_superuser_token_headers


class RealEnvBase:
    """Inheritable test real env base class with help functions"""

    def __init__(self):
        setup_logging()
        self.local_base_url = "http://localhost"
        self.api_v1_str = settings.API_V1_STR

    async def _get_superuser_token_headers(self) -> dict[str, str]:
        async with self._get_async_client() as c:
            superuser_token_headers = await get_superuser_token_headers(c)
            logger.debug("Superuser token headers: " + str(superuser_token_headers))
        return superuser_token_headers

    def _get_async_client(self) -> AsyncGenerator[AsyncClient, None]:
        """Use with all requests to the POM API"""
        return AsyncClient(app=app, base_url=self.local_base_url)
