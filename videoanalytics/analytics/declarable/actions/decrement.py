from videoanalytics.analytics.declarable.tools import Counter
from videoanalytics.models import Tracked


def decrement(counter: Counter, tracked: Tracked = None) -> None:
    counter.decrement()
