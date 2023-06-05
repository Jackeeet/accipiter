import queue

from videoanalytics.analytics.tools import Counter
from videoanalytics.models import Tracked


def increment(counter: Counter, output_queue: queue.Queue, tracked: Tracked = None) -> None:
    counter.increment()
    print(f"+1, current:{counter.value}")
