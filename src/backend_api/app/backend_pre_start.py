import asyncio
import logging

from sqlalchemy import select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.models.database import AsyncSessionFactory
from app.logs.logger import logger

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def init() -> None:
    try:
        async with AsyncSessionFactory.begin() as conn:
            await conn.execute(select(1))  # Check if DB is awake
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    asyncio.run(init())  # Run the async init function
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
