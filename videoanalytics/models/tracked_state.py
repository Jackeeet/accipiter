from enum import Flag, auto


class TrackedState(Flag):
    NONE = 0
    NEW = auto()
    ON_SCREEN = auto()
    CROSSING_LEFT = auto()
    CROSSING_RIGHT = auto()
    CROSSING_TOP = auto()
    CROSSING_BOTTOM = auto()
    IN_AREA = auto()


all_crossing_states = TrackedState.CROSSING_TOP | TrackedState.CROSSING_RIGHT | \
                      TrackedState.CROSSING_BOTTOM | TrackedState.CROSSING_LEFT
