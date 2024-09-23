import asyncio
import logging

from app.core.models.database import sessionmanager
from app.core.models.init_db import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    async with sessionmanager.session() as db:  # Use the session method from sessionmanager
        await init_db(db)


async def main() -> None:
    logger.info("Creating initial data")
    await init()
    logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())  # Run the async main function
