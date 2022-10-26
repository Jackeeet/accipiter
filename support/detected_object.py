# from support.object_state import ObjectState
import support.primitives as gp


class DetectedObject:
    def __init__(self, name, conf, x, y, w, h):
        self.name = name
        self.confidence = conf
        self.box = gp.Box(gp.Point(x, y), w, h)
        # self.state = ObjectState.INACTIVE

    def __repr__(self) -> str:
        return f'Object("{self.name}", {self.confidence}, {self.box.start.x}, {self.box.start.y}, {self.box.width}, {self.box.height}'
