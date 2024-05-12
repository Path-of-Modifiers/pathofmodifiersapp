import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
import requests
import os

BASEURL = os.getenv("DOMAIN")

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="backend_data_retrieval.log", encoding="utf-8", level=logging.INFO
)


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
        if "localhost" not in BASEURL:
            test_url = "https://" + BASEURL + "/api/api_v1/modifier/"
        else:
            test_url = "http://src-backend-1/api/api_v1/modifier/"
        response = requests.get(test_url)
        response.raise_for_status()
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
