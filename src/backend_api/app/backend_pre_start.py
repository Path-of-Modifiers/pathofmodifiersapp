import logging

from backend_api.app.core.models.database import SessionLocal
from backend_api.app.logs.logger import logger
from sqlalchemy import select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        # Try to create session to check if DB is awake
        db = SessionLocal()
        db.execute(select(1))
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
