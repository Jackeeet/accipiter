import queue

from logmanager.logmanager import LogManager
from videoanalytics.analytics.tools import Counter
from videoanalytics.models import Tracked


def increment(counter: Counter, output_queue: queue.Queue, logger: LogManager, tracked: Tracked = None) -> None:
    counter.increment()
