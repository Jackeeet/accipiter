from videoanalytics.analytics.tools import Counter
from videoanalytics.models import Tracked


def above(tracked: Tracked, counter: Counter, number: int) -> bool:
    return counter.value > number
