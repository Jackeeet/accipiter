from videoanalytics.analytics.tools import Counter
from videoanalytics.models import Tracked


def equals(tracked: Tracked, counter: Counter, number: int) -> bool:
    return counter.value == number


