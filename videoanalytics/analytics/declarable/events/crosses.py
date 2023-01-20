from videoanalytics.analytics.declarable.tools import Segment
from videoanalytics.analytics.geometry import segments_intersect
from videoanalytics.models import Tracked, Coords, TrackedState


def crosses(tracked: Tracked, segment: Segment) -> bool:
    b = tracked.obj.box
    diag1 = Segment(b.start, Coords(b.start.x + b.width, b.start.y + b.height))
    diag2 = Segment(Coords(b.start.x + b.width, b.start.y),
                    Coords(b.start.x, b.start.y + b.height))
    intersect = segments_intersect(diag1, segment) or segments_intersect(diag2, segment)

    new_intersection = False
    if not intersect:
        tracked.state = TrackedState.INACTIVE
    elif tracked.state != TrackedState.CROSSING:  # учитываем только первое пересечение линии объектом
        new_intersection = True
        tracked.state = TrackedState.CROSSING
    # if trackedState is already Crossing then just leave it at that

    # если объект пересекал эту же линию на предыдущих фреймах, действия выполнять не нужно
    return intersect and new_intersection
