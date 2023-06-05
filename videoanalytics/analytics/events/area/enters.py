from datetime import datetime

from videoanalytics.analytics.tools import Area
from videoanalytics.models import Tracked, TrackedState
from videoanalytics.models.tracked_state_helpers import disappeared


def enters(tracked: Tracked, area: Area) -> bool:
    if disappeared(tracked):
        return False

    inside = area.overlaps(tracked.obj.box)
    if not inside:
        return False

    last_area_state = tracked.states[area]
    result = last_area_state & TrackedState.IN_AREA == TrackedState.NONE
    tracked.states[area] |= TrackedState.IN_AREA

    if result:
        tracked.timers[area] = datetime.now()
    return result
