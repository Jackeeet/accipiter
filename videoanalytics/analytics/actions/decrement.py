import queue

from videoanalytics.analytics.tools import Counter
from videoanalytics.models import Tracked


def decrement(counter: Counter, output_queue: queue.Queue,tracked: Tracked = None) -> None:
    counter.decrement()
    print(f"-1, current:{counter.value}")
