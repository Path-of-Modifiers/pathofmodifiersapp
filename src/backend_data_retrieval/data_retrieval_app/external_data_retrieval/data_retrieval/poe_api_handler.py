import enum
import json
import logging
import threading
import time
from collections.abc import Iterator
from concurrent.futures import Future, ThreadPoolExecutor
from queue import Empty, Full, Queue
from typing import Literal

import httpx
import redis
from backend_api.app.core.schemas.currency import Currency
from backend_api.app.core.schemas.league import League
from pydantic import TypeAdapter

from data_retrieval_app.external_data_retrieval.config import settings
from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.external.poe import (
    Stash,
)
from data_retrieval_app.external_data_retrieval.data_retrieval.schemas.internal.categorized import (
    OrganizedItemsByCategory,
)
from data_retrieval_app.external_data_retrieval.data_retrieval.utils import (
    ByteResponse,
    RateLimiterThreadSafe,
)
from data_retrieval_app.external_data_retrieval.detectors.detector_controller import (
    DetectorController,
)
from data_retrieval_app.external_data_retrieval.detectors.unique_detector import (
    # UnidentifiedUniqueDetector,
    UniqueDetector,
)
from data_retrieval_app.external_data_retrieval.transforming_data.transform_poe_api_data import (
    PoEAPIDataTransformer,
)
from data_retrieval_app.external_data_retrieval.utils import (
    ProgramTooSlowException,
    sync_timing_tracker,
)
from data_retrieval_app.logs.logger import data_retrieval_logger as logger
from data_retrieval_app.utils import get_data_safe


class NextRequestState(enum.Enum):
    STOP = 1
    RESET = 2
    RETRY = 3
    READY = 4


class PoEAPIHandler:
    """
    Currently averages around 1.13s per request
    """

    headers = {
        "User-Agent": f"OAuth pathofmodifiers/{settings.TAG} (contact: {settings.OATH_ACC_TOKEN_CONTACT_EMAIL}) StrictMode"
    }

    def __init__(
        self,
        url: str,
        auth_token: str,
        *,
        leagues: list[League],
    ) -> None:
        """
        Parameters:
            :param url: (str) A string containing PoE public stash api url.
            :param auth_token: (str) A string containing OAuth2 auth token.
            :param item_detectors: (list[ItemDetector]) A list of `ItemDetector` instances.
        """
        logger.debug("Initializing PoEAPIHandler.")
        self.leagues = leagues
        self.data_transformer = PoEAPIDataTransformer(self.leagues)
        self.detector_controller = DetectorController(
            [
                UniqueDetector(),
                # UnidentifiedUniqueDetector(),
            ],
            leagues,
            self.data_transformer,
        )

        self.url = url
        logger.debug("Url set to: " + self.url)
        self.auth_token = auth_token
        self.headers["Authorization"] = "Bearer " + auth_token

        logger.debug("Headers set to: " + str(self.headers))

        self.stashes_adapter = TypeAdapter(list[Stash])

        self.skip_program_too_slow = False
        logger.info("PoEAPIHandler successfully initialized.")

    def _get_latest_change_id(self) -> str:
        """
        Gets the latest change id from GGG.
        The change id provided by GGG does not become available in the stream
        before 5 minutes. A manual next change id circumvents this wait.
        """

        # Can't have authorization header, so we make a new header
        headers = {
            "User-Agent": f"OAuth pathofmodifiers/0.1.0 (contact: {settings.OATH_ACC_TOKEN_CONTACT_EMAIL}) StrictMode"
        }
        response = get_data_safe(
            "https://www.pathofexile.com/api/trade/data/change-ids",
            headers=headers,
            logger=logger,
        )
        response_json = response.json()
        next_change_id = response_json["psapi"]
        logger.info(f"Retrieved latest change id: {next_change_id}. Sleeping for 310s")
        time.sleep(
            310
        )  # Sleeps for 5 minutes and 10 seconds (for safety) for the latest change id to be populated

        return next_change_id

    def _set_up_next_request(
        self,
        listener_id: int,
        sent_outgoing: bool,
        incoming: Queue,
        reset_event: threading.Event,
        stop_event: threading.Event,
        cache: redis.Redis,
    ) -> tuple[NextRequestState, str | None]:
        if stop_event.is_set():
            return NextRequestState.STOP, None
        if reset_event.is_set():
            logger.debug("Resetting the listener thread")
            change_id = None
            if listener_id == 0:
                logger.debug("Main listener initiating the ping-pong again")
                change_id = cache.get(f"next_change_id:{self.leagues[0].name}")
                if change_id is None:
                    change_id = self.initial_change_id
                    # Make sure second listener also resets
                time.sleep(5)
                reset_event.clear()
            return NextRequestState.RESET, change_id

        if sent_outgoing:
            try:
                # The timeout is to avoid getting stuck when the other listener has stopped
                change_id = incoming.get(timeout=5)
            except Empty:
                return NextRequestState.RETRY, None

            return NextRequestState.READY, change_id

        return NextRequestState.RETRY, None

    def _handle_response_error(
        self, response: httpx.Response, stop_event: threading.Event, weird_errors: int
    ) -> bool:
        # rate limited = 429 -> handled by ratelimiter
        if response.status_code == 503:
            # Temporarily unavailable = servers are down
            logger.critical(
                "Server is temporarily unavailable, sleeping for 30 seconds"
            )
            time.sleep(30)
            return
        else:
            response.read()
            logger.exception(
                f"Recieved the following response: status:'{response.status_code}' '{response.reason_phrase}' text:'{response.text}'"
            )
            response.raise_for_status()
            logger.warning(
                "The above response code did not result in an error, discarding the response for safety"
            )
            if weird_errors > 10:
                logger.exception(
                    "Too many unkown errors have occured, stopping current listener"
                )
                stop_event.set()
            return True

    def _follow_stream(
        self,
        listener_id: int,
        incoming: Queue,
        outgoing: Queue,
        reset_event: threading.Event,
        stop_event: threading.Event,
        cache: redis.Redis,
    ):
        logger.debug(f"Started listnener: {listener_id}")
        local_responses = []
        sent_outgoing = True
        weird_errors = 0
        default_retry_delay = 2
        retry_delay = default_retry_delay
        max_delay = 60
        try:
            while True:
                action, new_change_id = self._set_up_next_request(
                    listener_id, sent_outgoing, incoming, reset_event, stop_event, cache
                )
                match action:
                    case NextRequestState.STOP:
                        break
                    case NextRequestState.RESET:
                        continue
                    case NextRequestState.RETRY:
                        continue
                    case NextRequestState.READY:
                        change_id = new_change_id
                        retry_delay = default_retry_delay

                sent_outgoing = False

                self.rate_limiter.acquire()
                try:
                    with self.client.stream(
                        "GET", self.url, params={"id": change_id}
                    ) as response:
                        headers = response.headers
                        self.rate_limiter.update(headers)
                        if response.status_code >= 300:
                            is_weird_error = self._handle_response_error(
                                response, stop_event, weird_errors
                            )
                            if is_weird_error:
                                weird_errors += 1

                            continue

                        next_change_id = headers["X-Next-Change-Id"]
                        if next_change_id == change_id:
                            self.skip_program_too_slow = True
                            logger.info("We sucessfully caught up to the stream!")
                            time.sleep(30)
                            continue

                        try:
                            outgoing.put(next_change_id, timeout=5)
                            sent_outgoing = True
                        except Full:
                            continue

                        byte_response = ByteResponse(
                            change_id=change_id,
                            next_change_id=next_change_id,
                            response=response.read(),
                        )
                    local_responses.append(byte_response)
                except httpx.TransportError:
                    logger.warning(
                        f"Connection lost with server, backing off for {retry_delay} seconds",
                        exc_info=True,
                    )
                    time.sleep(retry_delay)
                    retry_delay = min(retry_delay * 2, max_delay)

                if len(local_responses) >= self.mini_batch_size // 2:
                    self._dump_responses(local_responses, stop_event)
        finally:
            logger.info(
                f"Listener {listener_id}: Exiting {self._follow_stream.__name__} gracefully"
            )
            self._dump_responses(local_responses, stop_event)
            if stop_event.is_set():
                self.response_queue.put(None)

    def _dump_responses(self, local_responses: list, stop_event: threading.Event):
        try:
            while local_responses and not stop_event.is_set():
                self.response_queue.put(local_responses[0], timeout=5)
                local_responses.pop(0)
        except Full:
            time.sleep(0.5)

    def initialize_data_stream_threads(
        self,
        n_listeners: int,
        executor: ThreadPoolExecutor,
        reset_event: threading.Event,
        stop_event: threading.Event,
        cache: redis.Redis,
        *,
        crashed: bool = False,
        listener_id: int = None,
    ) -> dict[Future, Literal["listener_0", "listener_1"]]:
        if settings.MANUAL_NEXT_CHANGE_ID:
            self.initial_change_id = settings.NEXT_CHANGE_ID
        else:
            league = self.leagues[0]["name"]
            self.initial_change_id = cache.get(f"next_change_id:{league}")
            if self.initial_change_id is None:
                logger.info("Using manually set change id")
                self.initial_change_id = self._get_latest_change_id()

        if not crashed:
            logger.info("Initializing follow stream threads")
            self.rate_limiter = RateLimiterThreadSafe()
            self.mini_batch_size = settings.MINI_BATCH_SIZE
            self.response_queue = Queue(maxsize=self.mini_batch_size)
            self.queues = [Queue(maxsize=1) for _ in range(n_listeners)]
            self.client = httpx.Client(
                http2=True,
                limits=httpx.Limits(
                    max_connections=n_listeners,
                    max_keepalive_connections=n_listeners,
                ),
                headers=self.headers,
            )
            logging.getLogger("httpx").setLevel(logging.WARNING)
        futures = {}
        for _listener_id in range(n_listeners):
            incoming = self.queues[_listener_id]
            outgoing = self.queues[
                _listener_id + 1 if _listener_id < (n_listeners - 1) else -1
            ]
            if not crashed or listener_id == _listener_id:
                future = executor.submit(
                    self._follow_stream,
                    _listener_id,
                    incoming,
                    outgoing,
                    reset_event,
                    stop_event,
                    cache,
                )
                futures[future] = f"listener_{_listener_id}"

        if not crashed:
            self.queues[0].put(self.initial_change_id)
        return futures

    @sync_timing_tracker
    def _read_stream(
        self, stop_event: threading.Event
    ) -> tuple[list[Stash], str | None]:
        i = 0
        stashes = list[Stash]()
        next_change_id = None
        while i < self.mini_batch_size:
            try:
                pending: ByteResponse | None = self.response_queue.get(timeout=5)
            except Empty:
                if self.response_queue.all_tasks_done and stop_event.is_set():
                    break
                continue

            # This is equivalent to a stop event, but ensures all stashes are processed
            if pending is None and self.response_queue.all_tasks_done:
                self.response_queue.task_done()
                return stashes, next_change_id
            elif pending is None:
                self.response_queue.task_done()
                continue

            obj = json.loads(pending.response.decode("utf-8"))
            _stashes = self.stashes_adapter.validate_python(obj["stashes"])
            # interesting_stashes = filter_by_owner(
            #     _stashes, "Bogadisa#6339"
            # )  # , "Kaaosvoima#6748"
            # if interesting_stashes is None:
            #     continue
            # print("stashes found!")
            # print(interesting_stashes)
            # stashes_to_json(pending.change_id, interesting_stashes)
            # continue
            stashes.extend(_stashes)
            self.response_queue.task_done()

            next_change_id = pending.next_change_id

            i += 1

        return stashes, next_change_id

    def _gather_n_checkpoints(
        self, n: int, stop_event: threading.Event
    ) -> tuple[OrganizedItemsByCategory, str]:
        all_organized_items = OrganizedItemsByCategory()
        for _ in range(n):
            start_time = time.perf_counter()
            stashes, next_change_id = self._read_stream(stop_event)
            organized_items = self.detector_controller.filter_stashes(stashes)
            end_time = time.perf_counter()

            time_per_mini_batch = end_time - start_time
            if time_per_mini_batch > settings.MAX_TIME_PER_MINI_BATCH:
                if self.skip_program_too_slow:
                    # Program sleeps when we have caught up to stream, making it
                    # too easy to trigger `ProgramTooSlowException`
                    self.skip_program_too_slow = False
                else:
                    # Does not allow a batch to take longer than 2 minutes
                    raise ProgramTooSlowException

            all_organized_items.extend(organized_items)
            if stop_event.is_set():
                break

        return all_organized_items, next_change_id

    def dump_stream(
        self,
        cache: redis.Redis,
        current_hours: dict[int, int],
        currencies: dict[tuple[int, str], Currency],
        stop_event: threading.Event,
    ) -> Iterator[str | None]:
        self.redis_cache = cache
        self.detector_controller.set_redis_cache(self.redis_cache)

        self.data_transformer.set_current_hours(current_hours)
        self.data_transformer.set_currencies(currencies)

        while True and not stop_event.is_set():
            logger.info("Waiting for data from the stream")
            organized_items, next_change_id = self._gather_n_checkpoints(
                n=settings.N_CHECKPOINTS_PER_TRANSFORMATION, stop_event=stop_event
            )
            if organized_items.is_empty():
                logger.info("Found no data")
                continue
            logger.info("Finished processing the stream, entering transformation phase")
            self.data_transformer.transform_and_insert(organized_items)
            logger.info("Finished transformation phase")
            yield next_change_id

    def end_of_hour_cleanup(self):
        self.data_transformer.end_of_hour_cleanup()

    def end_of_program_cleanup(self):
        self.detector_controller.end_of_program_cleanup()
