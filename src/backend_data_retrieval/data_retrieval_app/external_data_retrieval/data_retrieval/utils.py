import threading
import time
from collections import deque
from dataclasses import dataclass

import httpx


@dataclass
class PendingResponse:
    change_id: str
    next_change_id: str
    response: bytes


class RateLimiterThreadSafe:
    def __init__(self):
        self.lock = threading.Condition()

        self.max_hits = 2
        self.period = 1

        self.sent = deque()

        # Absolute authority from server.
        self.block_until = 0.0

    def acquire(self):
        with self.lock:
            while True:
                now = time.monotonic()

                # Server says we're blocked.
                if now < self.block_until:
                    self.lock.wait(self.block_until - now)
                    continue

                # Forget expired timestamps.
                while self.sent and (now - self.sent[0]) >= self.period:
                    self.sent.popleft()

                if len(self.sent) < self.max_hits:
                    self.sent.append(now)
                    return

                wait = self.period - (now - self.sent[0])
                self.lock.wait(wait)

    def update(self, headers: httpx.Headers):
        now = time.monotonic()

        rule = headers.get("X-Rate-Limit-Ip")
        state = headers.get("X-Rate-Limit-Ip-State")

        if not rule or not state:
            return

        max_hits, period, restricted = map(int, rule.split(":"))
        hits, _, active = map(int, state.split(":"))

        with self.lock:
            self.max_hits = max_hits
            self.period = period

            # Server restriction overrides everything.
            if active:
                self.block_until = now + active
            else:
                self.block_until = 0

            # Reconcile our local accounting with the server.
            # If the server believes we've already used more requests
            # than we have recorded, pad our deque with "now".
            while len(self.sent) < hits:
                self.sent.append(now)

            while len(self.sent) > hits:
                self.sent.popleft()

            self.lock.notify_all()


class RateLimiter:
    def __init__(self):
        self.max_hits = 2
        self.period = 1

        self.sent = []

        # Absolute authority from server.
        self.block_until = 0.0

    def acquire(self):
        while True:
            now = time.monotonic()

            # Server says we're blocked.
            if now < self.block_until:
                time.sleep(self.block_until - now)
                continue

            # Forget expired timestamps.
            while self.sent and (now - self.sent[0]) >= self.period:
                self.sent.pop(0)

            if len(self.sent) < self.max_hits:
                self.sent.append(now)
                return

            wait = self.period - (now - self.sent[0])
            time.sleep(wait)

    def update(self, headers: httpx.Headers):
        now = time.monotonic()

        rule = headers.get("X-Rate-Limit-Ip")
        state = headers.get("X-Rate-Limit-Ip-State")

        if not rule or not state:
            return

        max_hits, period, restricted = map(int, rule.split(":"))
        hits, _, active = map(int, state.split(":"))

        self.max_hits = max_hits
        self.period = period

        # Server restriction overrides everything.
        if active:
            self.block_until = now + active
        else:
            self.block_until = 0

        # Reconcile our local accounting with the server.
        # If the server believes we've already used more requests
        # than we have recorded, pad our deque with "now".
        while len(self.sent) < hits:
            self.sent.append(now)

        while len(self.sent) > hits:
            self.sent.pop(0)
