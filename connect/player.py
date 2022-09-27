from abc import ABC, abstractmethod
from threading import Thread, Event
import time
import queue


class Player(ABC):

    def move(self, board, depth=None, heuristic=None, timeout=None):
        """Request a move within the given number of seconds."""
        if timeout is None:
            return self._move(board, depth, heuristic, None)

        timeout_event = Event()
        que = queue.Queue()

        thread = Thread(
                target = lambda q, *args: q.put(self._move(*args)),
                args = (que, board, depth, heuristic, timeout_event)
        )

        thread.start()
        thread.join(timeout)

        if thread.is_alive():
            timeout_event.set()
            thread.join()
            return que.get()
        else:
            return que.get()


    @abstractmethod
    def _move(self, board, depth=None, heuristic=None, timeout=None):
        pass
