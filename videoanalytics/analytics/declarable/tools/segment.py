import cv2

from videoanalytics.analytics.declarable.tools import Tool
from videoanalytics.models import Coords


class Segment(Tool):
    def __init__(self, start: Coords, end: Coords, colour: tuple[int, int, int] = None, thickness: int = 2) -> None:
        self.start = start
        self.end = end
        super().__init__(colour, thickness)

    def draw_on(self, image):
        cv2.line(image, self.start, self.end, self.colour, thickness=self.thickness)
