from videoanalytics.objectmodels.detected import Detected
from .tracked_state import TrackedState


class Tracked:
    max_FTL = 1

    def __init__(self, obj: Detected) -> None:
        self.id = obj.box.start
        self.obj = obj
        self.FTL = self.max_FTL
        self.state = TrackedState.INACTIVE

    def __repr__(self) -> str:
        return f"id: {self.id} FTL: {self.FTL}"
