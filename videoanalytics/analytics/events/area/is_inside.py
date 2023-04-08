from videoanalytics.analytics.tools import Area
from videoanalytics.models import Tracked, TrackedState


def is_inside(tracked: Tracked, area: Area) -> bool:
    inside = area.contains(tracked.obj.box)
    if inside:
        tracked.states[area] |= TrackedState.IN_AREA
    else:
        tracked.states[area] &= ~TrackedState.IN_AREA
    return inside
