from typing import Callable

from videoanalytics.analytics.declarable.events.event import Event
from videoanalytics.models import Tracked


class EventChain:
    def __init__(self, left=None, val: Event | Callable[[bool, bool], bool] = None, right=None) -> None:
        self.left = left
        self.value = val
        self.right = right

    def check(self, tracked: Tracked) -> bool:
        if self.left is None and self.right is None:
            return self.value.check(tracked)
        elif self.left is None or self.right is None:
            raise ValueError("missing an operand")
        else:
            return self.value(self.left.check(tracked), self.right.check(tracked))
            # could probably implement short-circuiting here
