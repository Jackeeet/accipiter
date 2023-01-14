from typing import Any, Callable

from .tools import Coords, Segment
from ..geometry import segments_intersect
from ...models import Tracked, TrackedState


class Event:
    def __init__(self, event: Callable, object_kind: str, params: dict[str, Any]) -> None:
        self._check_event = event
        self._object_kind = object_kind
        self._params = params

    def check(self, tracked: Tracked) -> bool:
        if tracked.obj.name != self._object_kind:
            return False
        return self._check_event(tracked, **self._params)


def intersects(tracked: Tracked, seg: Segment) -> bool:
    b = tracked.obj.box
    diag1 = Segment(b.start, Coords(b.start.x + b.width, b.start.y + b.height))
    diag2 = Segment(Coords(b.start.x + b.width, b.start.y),
                    Coords(b.start.x, b.start.y + b.height))
    intersect = segments_intersect(diag1, seg) or segments_intersect(diag2, seg)

    new_intersection = False
    if not intersect:
        tracked.state = TrackedState.INACTIVE
    elif tracked.state != TrackedState.CROSSING:  # учитываем только первое пересечение линии объектом
        new_intersection = True
        tracked.state = TrackedState.CROSSING
    # if trackedState is already Crossing then just leave it at that

    # если объект пересекал эту же линию на предыдущих фреймах, действия выполнять не нужно
    return intersect and new_intersection


def op_and(left: bool, right: bool) -> bool:
    return left and right


def op_or(left: bool, right: bool) -> bool:
    return left or right


class BinaryEventChain:
    def __init__(self, left=None, val: Event | Callable[[bool, bool], bool] = None, right=None) -> None:
        self.left = left
        self.value = val
        self.right = right

    def check(self, object: Tracked) -> bool:
        if self.left is None and self.right is None:
            return self.value.check(object)
        elif self.left is None or self.right is None:
            raise ValueError("missing an operand")
        else:
            return self.value(self.left.check(object), self.right.check(object))
            # could probably implement short-circuiting here
