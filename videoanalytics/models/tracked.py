from videoanalytics.analytics.declarable.tools.abstract import Markup
from videoanalytics.models.detected import Detected
from videoanalytics.models.tracked_state import TrackedState


class Tracked:
    states: dict[Markup, TrackedState]
    max_FTL = 1

    def __init__(self, obj: Detected, markup: list[Markup]) -> None:
        self.id = obj.box.start
        self.obj = obj
        self.FTL = self.max_FTL
        self.states = {m: TrackedState.NONE for m in markup}

    def __repr__(self) -> str:
        return f"id: {self.id} FTL: {self.FTL}"
