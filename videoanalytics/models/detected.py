from cv2 import rectangle, putText, FONT_HERSHEY_SIMPLEX
from . import Box, Coords


class Detected:
    def __init__(self, name, conf, x, y, w, h, colour=None) -> None:
        self.name = name
        self.confidence = conf
        self.box = Box(Coords(x, y), w, h)
        self.colour = colour or 123

    def __repr__(self) -> str:
        return f'DetectedObject("{self.name}", {self.confidence}, {self.box.start.x}, {self.box.start.y}, {self.box.width}, {self.box.height}'

    def draw(self, frame) -> None:
        top_left = (self.box.start.x, self.box.start.y)
        bottom_right = (self.box.start.x + self.box.width,
                        self.box.start.y + self.box.height)
        rectangle(frame, top_left, bottom_right, self.colour, 2)
        putText(frame, self.name, (self.box.start.x, self.box.start.y - 10),
                FONT_HERSHEY_SIMPLEX, 0.5, self.colour, 2)
