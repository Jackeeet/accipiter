import cv2

from videoanalytics.analytics.declarable.tools import Tool
from videoanalytics.models import Coords


class Curve(Tool):
    def __init__(self, center: Coords, radius: int, start: int, end: int, colour: tuple[int, int, int] = None,
                 thickness: int = 2):
        self.center = center
        self.major_axis = radius
        self.minor_axis = radius
        self.start = start
        self.end = end
        super().__init__(colour, thickness)

    def draw_on(self, image):
        cv2.ellipse(image, self.center, (self.major_axis, self.minor_axis),
                    0, self.start, self.end, self.colour, self.thickness)
