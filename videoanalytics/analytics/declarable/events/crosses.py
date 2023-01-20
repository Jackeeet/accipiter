from videoanalytics.analytics.declarable.tools import Segment
from videoanalytics.analytics.geometry import segments_intersect
from videoanalytics.models import Tracked, TrackedState


def crosses(tracked: Tracked, segment: Segment) -> bool:
    crossed = segments_intersect(tracked.obj.left, segment) or \
              segments_intersect(tracked.obj.right, segment) or \
              segments_intersect(tracked.obj.top, segment) or \
              segments_intersect(tracked.obj.bottom, segment)

    state_changed = False
    if not crossed:
        tracked.state = TrackedState.INACTIVE
    elif tracked.state != TrackedState.CROSSING:  # учитываем только первое пересечение линии объектом
        state_changed = True
        tracked.state = TrackedState.CROSSING
    # if trackedState is already Crossing then just leave it at that

    # если объект пересекал эту же линию на предыдущих фреймах, действия выполнять не нужно
    return crossed and state_changed
