from datetime import datetime

from videoanalytics.analytics.tools import Area
from videoanalytics.models import Tracked, TrackedState


def enters(tracked: Tracked, area: Area) -> bool:
    inside = area.contains(tracked.obj.box)
    if not inside:
        return False

    last_area_state = tracked.states[area]
    result = last_area_state & TrackedState.IN_AREA == TrackedState.NONE
    tracked.states[area] |= TrackedState.IN_AREA

    if result:
        tracked.timers[area] = datetime.now()
        print('enters')
        # print('+++++++++++++++++')
        # print(f'set time: {tracked.timers[area]}')
        # print(f'last area state: {last_area_state}')
        # print(f'new area state: {tracked.states[area]}')
        # print('+++++++++++++++++')

    return result
