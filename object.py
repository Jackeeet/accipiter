from collections import namedtuple

Box = namedtuple("Box", "x y width height")


class Object:
    def __init__(self, name, conf, x, y, w, h):
        self.name = name
        self.confidence = conf
        self.box = Box(x, y, w, h)

    def __repr__(self) -> str:
        return f'Object("{self.name}", {self.confidence}, {self.box.x}, {self.box.y}, {self.box.width}, {self.box.height}'
