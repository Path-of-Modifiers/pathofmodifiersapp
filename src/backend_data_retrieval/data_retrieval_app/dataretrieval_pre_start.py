import logging

import requests
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.logs.logger import main_logger as logger
from data_retrieval_app.pom_api_authentication import get_superuser_token_headers

max_tries = 60 * 5  # 5 minutes
wait_seconds = 6


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
        logger.debug(
            "The following error occurred while initializing pom api request:", e
        )
        raise e


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
