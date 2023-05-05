from videoanalytics.models import Tracked
from videoanalytics.models.side import SideValue
from videoanalytics.models.tracked_state import TrackedState


def object_crossing_state(obj_sides_crossing: dict[SideValue, bool]) -> TrackedState:
    state = TrackedState.NONE
    if obj_sides_crossing[SideValue.LEFT]:
        state |= TrackedState.CROSSING_LEFT
    if obj_sides_crossing[SideValue.RIGHT]:
        state |= TrackedState.CROSSING_RIGHT
    if obj_sides_crossing[SideValue.TOP]:
        state |= TrackedState.CROSSING_TOP
    if obj_sides_crossing[SideValue.BOTTOM]:
        state |= TrackedState.CROSSING_BOTTOM
    return state


def disappeared(tracked: Tracked) -> bool:
    return (tracked.states[next(iter(tracked.states))] & TrackedState.DISAPPEARED) == TrackedState.DISAPPEARED
