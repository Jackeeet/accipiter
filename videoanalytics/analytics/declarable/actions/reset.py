from videoanalytics.analytics.declarable.tools import Counter
from videoanalytics.models import Tracked


def reset(counter: Counter, tracked: Tracked = None) -> None:
    counter.reset()
