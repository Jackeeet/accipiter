from enum import StrEnum, auto

from videoanalytics.interfaces.logical import Logical
from videoanalytics.models.operators import op_bitwise_or
from videoanalytics.models.tracked_state import TrackedState


class SideValue(StrEnum):
    LEFT = auto()
    RIGHT = auto()
    TOP = auto()
    BOTTOM = auto()


class Side(Logical):
    def __init__(self, value: SideValue) -> None:
        self.value = value

    def evaluate(self, **values) -> TrackedState:
        return self.to_crossing_state()

    def __repr__(self):
        return f"Side({self.value})"

    @staticmethod
    def op_and(left: TrackedState, right: TrackedState) -> TrackedState:
        return op_bitwise_or(left, right)

    @staticmethod
    def op_or(left: TrackedState, right: TrackedState) -> TrackedState:
        # the return value is INTENTIONALLY the same as the return value of op_and
        return op_bitwise_or(left, right)

    def to_crossing_state(self) -> TrackedState:
        match self.value:
            case SideValue.LEFT:
                return TrackedState.CROSSING_LEFT
            case SideValue.RIGHT:
                return TrackedState.CROSSING_RIGHT
            case SideValue.TOP:
                return TrackedState.CROSSING_TOP
            case SideValue.BOTTOM:
                return TrackedState.CROSSING_BOTTOM
