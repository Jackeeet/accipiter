from enum import Flag, auto

from videoanalytics.models import SideValue


class TrackedState(Flag):
    NONE = 0
    ON_SCREEN = auto()
    CROSSING_LEFT = auto()
    CROSSING_RIGHT = auto()
    CROSSING_TOP = auto()
    CROSSING_BOTTOM = auto()


all_crossing_states = TrackedState.CROSSING_TOP | TrackedState.CROSSING_RIGHT | \
                      TrackedState.CROSSING_BOTTOM | TrackedState.CROSSING_LEFT


def side_value_to_crossing_state(side: SideValue) -> TrackedState:
    match side:
        case SideValue.LEFT:
            return TrackedState.CROSSING_LEFT
        case SideValue.RIGHT:
            return TrackedState.CROSSING_RIGHT
        case SideValue.TOP:
            return TrackedState.CROSSING_TOP
        case SideValue.BOTTOM:
            return TrackedState.CROSSING_BOTTOM


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
