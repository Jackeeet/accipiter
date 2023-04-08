from videoanalytics.analytics.tools import Area
from videoanalytics.models import Tracked, TrackedState


def leaves(tracked: Tracked, area: Area) -> bool:
    inside = area.contains(tracked.obj.box)
    if inside:
        return False
    last_area_state = tracked.states[area]
    result = last_area_state & TrackedState.IN_AREA != TrackedState.NONE
    last_area_state &= ~TrackedState.IN_AREA
    return result
