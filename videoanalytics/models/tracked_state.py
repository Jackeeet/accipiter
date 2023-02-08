from enum import Flag, auto


class TrackedState(Flag):
    NONE = 0
    ON_SCREEN = auto()
    CROSSING_LEFT = auto()
    CROSSING_RIGHT = auto()
    CROSSING_TOP = auto()
    CROSSING_BOTTOM = auto()
    ENTERING_AREA = auto()
    INSIDE_AREA = auto()
    LEAVING_AREA = auto()


all_crossing_states = TrackedState.CROSSING_TOP \
                      | TrackedState.CROSSING_RIGHT \
                      | TrackedState.CROSSING_BOTTOM \
                      | TrackedState.CROSSING_LEFT

all_area_states = TrackedState.ENTERING_AREA \
                  | TrackedState.INSIDE_AREA \
                  | TrackedState.LEAVING_AREA

