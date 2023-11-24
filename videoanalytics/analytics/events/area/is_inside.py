from datetime import datetime

from videoanalytics.analytics.tools import Area
from videoanalytics.models import Tracked, TrackedState
from videoanalytics.models.tracked_state_helpers import disappeared


def is_inside(tracked: Tracked, area: Area, period: int) -> bool:
    if disappeared(tracked):
        return False

    in_area = area.contains(tracked.obj.box)

    if period is None:
        inside = in_area
    elif in_area:
        if area in tracked.timers:
            in_area_time = datetime.now() - tracked.timers[area]
            period_passed = in_area_time.total_seconds() >= period
            inside = period_passed
        else:
            tracked.timers[area] = datetime.now()
            inside = False
    else:
        inside = False

    if inside:
        tracked.states[area] |= TrackedState.IN_AREA
        tracked.timers.pop(area, None)
    return inside
