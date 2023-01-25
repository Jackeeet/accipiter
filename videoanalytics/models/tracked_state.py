from enum import Flag, auto


class TrackedState(Flag):
    NONE = auto()
    CROSSING_LEFT = auto()
    CROSSING_RIGHT = auto()
    CROSSING_TOP = auto()
    CROSSING_BOTTOM = auto()


crossing_states = TrackedState.CROSSING_TOP | TrackedState.CROSSING_RIGHT | \
                  TrackedState.CROSSING_BOTTOM | TrackedState.CROSSING_LEFT


def get_crossing_state(bottom: bool, left: bool, right: bool, top: bool) -> TrackedState:
    state = TrackedState.NONE
    if left:
        state |= TrackedState.CROSSING_RIGHT
    if right:
        state |= TrackedState.CROSSING_LEFT
    if top:
        state |= TrackedState.CROSSING_BOTTOM
    if bottom:
        state |= TrackedState.CROSSING_TOP
    return state
