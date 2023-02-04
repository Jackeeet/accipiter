from enum import StrEnum, auto

from videoanalytics.analytics.interfaces import Evaluable


class SideValue(StrEnum):
    LEFT = auto()
    RIGHT = auto()
    TOP = auto()
    BOTTOM = auto()


class Side(Evaluable):
    def __init__(self, value: SideValue) -> None:
        self.value = value

    def evaluate(self, **values) -> bool:
        if 'obj_crossing_state' not in values:
            raise ValueError()  # todo add message
        obj_sides_crossing: dict[SideValue, bool] = values['obj_crossing_state']
        return obj_sides_crossing[self.value]
