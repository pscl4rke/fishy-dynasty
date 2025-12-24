

import asyncio
from contextlib import contextmanager


class Fan:

    def __init__(self):
        self._listeners = set()

    def publish(self, value):
        for queue in self._listeners:
            queue.put_nowait(value)

    @contextmanager
    def subscribe(self):
        try:
            queue = asyncio.Queue()
            self._listeners.add(queue)
            yield queue
        finally:
            self._listeners.remove(queue)
