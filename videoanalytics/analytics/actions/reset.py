import queue

from videoanalytics.analytics.tools import Counter
from videoanalytics.models import Tracked


def reset(counter: Counter, output_queue: queue.Queue, tracked: Tracked = None) -> None:
    counter.reset()
