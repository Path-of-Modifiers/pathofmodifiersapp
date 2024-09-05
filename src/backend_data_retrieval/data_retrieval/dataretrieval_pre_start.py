import logging

import requests
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from external_data_retrieval.config import settings
from pom_api_authentication import get_superuser_token_headers

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
        pom_api_headers = {}
        if "localhost" not in settings.BASEURL:
            test_url = "https://" + settings.BASEURL + "/api/api_v1/modifier/"
            pom_api_headers = get_superuser_token_headers(
                "https://" + settings.BASEURL + "/api/api_v1"
            )
        else:
            test_url = "http://src-backend-1/api/api_v1/modifier/"
            pom_api_headers = get_superuser_token_headers(
                "http://src-backend-1/api/api_v1"
            )
        response = requests.get(test_url, headers=pom_api_headers)
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
