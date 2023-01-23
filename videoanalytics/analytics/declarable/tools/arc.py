import math
import cv2

from videoanalytics.analytics.declarable.tools import Tool
from videoanalytics.models import Coords


class Arc(Tool):
    def __init__(self, center: Coords, radius: int, start_angle: int, end_angle: int,
                 colour: tuple[int, int, int] = None,
                 thickness: int = 2):
        super().__init__(colour, thickness)
        self.center = center
        self.radius = radius
        self.major_axis = radius
        self.minor_axis = radius
        self.start_angle = start_angle % 360
        self.end_angle = end_angle % 360

        ea = self.end_angle + 360 if self.end_angle < self.start_angle else self.end_angle
        self.angle = ea - self.start_angle

    @property
    def start(self) -> Coords:
        s = math.radians(self.start_angle)
        return Coords(
            self.center.x + round(self.radius * math.cos(s)),
            self.center.y + round(self.radius * -math.sin(s))
        )

    @property
    def end(self) -> Coords:
        e = math.radians(self.end_angle)
        return Coords(
            self.center.x + round(self.radius * math.cos(e)),
            self.center.y + round(self.radius * -math.sin(e))
        )

    @property
    def normalized(self) -> 'Arc':
        """  Нормализованная дуга c теми же параметрами, что и исходная.

        :return: дуга с центром в точке (0,0)
        """
        return Arc(Coords(0, 0), self.radius, self.start_angle, self.end_angle,
                   self.colour, self.thickness)

    @property
    def is_minor(self) -> bool:
        """ Определяет, является ли дуга меньшей дугой окружности.

        :return: True, если дуга меньше 180 градусов, иначе False
        """
        return self.angle < 180

    @property
    def is_semicircular(self) -> bool:
        return self.angle == 180

    def draw_on(self, image):
        cv2.ellipse(
            image, self.center, (self.major_axis, self.minor_axis), 0,
            self.start_angle, self.end_angle,
            self.colour, self.thickness
        )

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Arc):
            return self.center == o.center and self.radius == o.radius \
                   and self.start_angle == o.start_angle and self.end_angle == o.end_angle

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __repr__(self) -> str:
        return f"Arc({self.center}, {self.radius}, {self.start_angle}, {self.end_angle})"
