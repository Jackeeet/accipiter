from cv2 import rectangle, putText, FONT_HERSHEY_COMPLEX

from videoanalytics.analytics.tools import Segment
from videoanalytics.models import Box, Coords


class Detected:
    def __init__(self, name, conf, x, y, w, h, colour=None) -> None:
        self.name = name
        self.confidence = conf
        self.box = Box(Coords(x, y), w, h)
        self.colour = colour or 123

    @property
    def top_left(self) -> Coords:
        return self.box.start

    @property
    def top_right(self) -> Coords:
        return Coords(self.box.start.x + self.box.width, self.box.start.y)

    @property
    def bottom_left(self) -> Coords:
        return Coords(self.box.start.x, self.box.start.y + self.box.height)

    @property
    def bottom_right(self) -> Coords:
        return Coords(self.box.start.x + self.box.width, self.box.start.y + self.box.height)

    @property
    def top(self) -> Segment:
        return Segment(self.top_left, self.top_right)

    @property
    def right(self) -> Segment:
        return Segment(self.top_right, self.bottom_right)

    @property
    def bottom(self) -> Segment:
        return Segment(self.bottom_left, self.bottom_right)

    @property
    def left(self):
        return Segment(self.top_left, self.bottom_left)

    def __repr__(self) -> str:
        return f'DetectedObject("{self.name}", {round(self.confidence, 2)}, ' \
               f'{self.box.start.x}, {self.box.start.y}, {self.box.width}, {self.box.height})'

    def draw(self, frame) -> None:
        top_left = (self.top_left.x, self.top_left.y)
        bottom_right = (self.bottom_right.x, self.bottom_right.y)
        rectangle(frame, top_left, bottom_right, self.colour, 2)
        putText(frame, f"{self.name}", (self.box.start.x, self.box.start.y - 10),
                FONT_HERSHEY_COMPLEX, 0.5, self.colour, 2)
