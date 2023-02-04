from videoanalytics.analytics.tools import Counter
from videoanalytics.models import Tracked


def increment(counter: Counter, tracked: Tracked = None) -> None:
    counter.increment()
