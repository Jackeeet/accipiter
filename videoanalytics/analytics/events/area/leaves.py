from videoanalytics.analytics.tools import Area
from videoanalytics.models import Tracked, TrackedState
from videoanalytics.models.tracked_state_helpers import disappeared


def leaves(tracked: Tracked, area: Area) -> bool:
    if disappeared(tracked):
        return True

    inside = area.contains(tracked.obj.box)
    if inside:
        return False

    last_area_state = tracked.states[area]
    result = last_area_state & TrackedState.IN_AREA != TrackedState.NONE
    tracked.states[area] &= ~TrackedState.IN_AREA

    if result:
        tracked.timers.pop(area, None)
        print('leaves')

    return result
