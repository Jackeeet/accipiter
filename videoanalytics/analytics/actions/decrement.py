import queue

from logmanager.logmanager import LogManager
from videoanalytics.analytics.tools import Counter
from videoanalytics.models import Tracked


def decrement(counter: Counter, output_queue: queue.Queue, logger: LogManager,tracked: Tracked = None) -> None:
    counter.decrement()
    print(f"-1, current:{counter.value}")
