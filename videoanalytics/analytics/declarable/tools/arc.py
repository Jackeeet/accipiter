import cv2

from videoanalytics.analytics.declarable.tools import Tool
from videoanalytics.models import Coords


class Arc(Tool):
    def __init__(self, center: Coords, radius: int, start_angle: int, end_angle: int,
                 colour: tuple[int, int, int] = None,
                 thickness: int = 2):
        self.center = center
        self.radius = radius
        self.major_axis = radius
        self.minor_axis = radius
        self.start_angle = start_angle % 360
        self.end_angle = end_angle % 360
        super().__init__(colour, thickness)

    @property
    def start(self) -> Coords:
        raise NotImplementedError

    @property
    def end(self) -> Coords:
        raise NotImplementedError

    @property
    def normalized(self) -> 'Arc':
        """  Нормализованная дуга c теми же параметрами, что и исходная.

        :return: дуга с центром в точке (0,0)
        """
        return Arc(Coords(0, 0), self.radius, self.start_angle, self.end_angle,
                   self.colour, self.thickness)

    def draw_on(self, image):
        cv2.ellipse(
            image, self.center, (self.major_axis, self.minor_axis), 0,
            self.start_angle, self.end_angle,
            self.colour, self.thickness
        )
