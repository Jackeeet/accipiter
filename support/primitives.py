import cv2
import random
from collections import namedtuple

Point = namedtuple("Point", "x y")

Box = namedtuple("Box", "start width height")


class Segment:
    def __init__(self, start: Point, end: Point, thickness=2, color=None) -> None:
        self.start = start
        self.end = end

        self.thickness = thickness
        self.color = color or (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

    def draw_on(self, image):
        cv2.line(image, self.start, self.end,
                 self.color, thickness=self.thickness)


class Text:
    def __init__(self, origin: Point):
        self.origin = origin
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.scale = 1
        self.color = (0, 0, 0)
        self.thickness = 2
        self.line = cv2.LINE_AA

    def draw_on(self, image, text):
        cv2.putText(image, text, self.origin, self.font,
                    self.scale, self.color, self.thickness, self.line)
