from datetime import datetime

from videoanalytics.analytics.tools import Area
from videoanalytics.analytics.tools.abstract import Markup
from videoanalytics.models.detected import Detected
from videoanalytics.models.tracked_state import TrackedState


class Tracked:
    states: dict[Markup, TrackedState]
    timers: dict[Area, datetime]

    max_FTL = 10

    id = 0

    def __init__(self, obj: Detected, markup: list[Markup]) -> None:
        self._act_id = Tracked.id
        Tracked.id += 1
        self.obj = obj
        self.FTL = self.max_FTL
        self.states = {m: TrackedState.NONE for m in markup}
        self.states[markup[0]] |= TrackedState.NEW
        self.timers = dict()
        self.event_colour = None
        self.event_colour_FTL = 0

    def __repr__(self) -> str:
        return f"id: {self._act_id} FTL: {self.FTL}"
