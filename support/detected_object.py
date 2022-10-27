import support.primitives as gp
from support.tracked_state import TrackedState


class Detected:
    def __init__(self, name, conf, x, y, w, h) -> None:
        self.name = name
        self.confidence = conf
        self.box = gp.Box(gp.Point(x, y), w, h)

    def __repr__(self) -> str:
        return f'DetectedObject("{self.name}", {self.confidence}, {self.box.start.x}, {self.box.start.y}, {self.box.width}, {self.box.height}'


class Tracked:
    max_FTL = 1

    def __init__(self, obj: Detected) -> None:
        self.id = obj.box.start
        self.obj = obj
        self.FTL = self.max_FTL
        self.state = TrackedState.INACTIVE
        # self.num = 0

    def __str__(self) -> str:
        return f"id: {self.id} FTL: {self.FTL}"
