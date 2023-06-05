import cv2
import numpy as np
from numpy import sqrt

from videoanalytics.analytics.tools.abstract import Component
from videoanalytics.analytics.tools.interfaces import Intersectable
from videoanalytics.models import Coords


class Segment(Component, Intersectable):
    def __init__(
            self, start: Coords, end: Coords, colour: tuple[int, int, int] = None, thickness: int = 2
    ) -> None:
        self._start = start
        self._end = end
        super().__init__(colour, thickness)

    def draw_on(self, image) -> None:
        cv2.line(image, self.start.xy, self.end.xy, self.colour, thickness=self.thickness)

    def intersects(self, segment) -> bool:
        return Segment.segments_intersect(segment, self)

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def length(self):
        return sqrt((self._start.x - self._end.x) ** 2 + (self._start.y - self.end.y) ** 2)

    @property
    def director(self):
        x = (self._start.x - self._end.x) / self.length
        y = (self._start.y - self._end.y) / self.length
        return Coords(x, y)

    @property
    def bounding_box(self):
        min_x = min(self._start.x, self._end.x)
        min_y = min(self._start.y, self._end.y)
        max_x = max(self._start.x, self._end.x)
        max_y = max(self._start.y, self._end.y)
        return Segment(Coords(min_x, min_y), Coords(max_x, max_y))

    def translated(self, translation, vertical):
        if vertical:
            return Segment(
                Coords(self.start.x, self.start.y + translation),
                Coords(self.end.x, self.end.y + translation)
            )
        return Segment(
            Coords(self.start.x + translation, self.start.y),
            Coords(self.end.x + translation, self.end.y)
        )

    def start_to_point(self, point):
        return Segment(self.start, point)

    def end_to_point(self, point):
        return Segment(self.end, point)

    def extend_x(self, value):
        return Segment(
            Coords(self.start.x - value, self.start.y),
            Coords(self.end.x + value, self.end.y)
        )

    def extend_y(self, value):
        return Segment(
            Coords(self.start.x, self.start.y - value),
            Coords(self.end.x, self.end.y + value)
        )

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Segment):
            return self.start == o.start and self.end == o.end
        return False

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __repr__(self) -> str:
        return f"Segment({self.start}, {self.end})"

    def __hash__(self) -> int:
        return hash((self.start, self.end))

    @staticmethod
    def segments_intersect(s1: 'Segment', s2: 'Segment') -> bool:
        """ Определяет, пересекаются ли два отрезка.

        :param s1: Первый отрезок
        :param s2: второй отрезок
        :return: True, если отрезки пересекаются, иначе False
        """
        p341 = (s2.start, s2.end, s1.start)
        p342 = (s2.start, s2.end, s1.end)
        p123 = (s1.start, s1.end, s2.start)
        p124 = (s1.start, s1.end, s2.end)

        d1 = Segment.direction(*p341)
        d2 = Segment.direction(*p342)
        d3 = Segment.direction(*p123)
        d4 = Segment.direction(*p124)

        p12_straddles_p34 = d1 > 0 > d2 or d1 < 0 < d2
        p34_straddles_p12 = d3 > 0 > d4 or d3 < 0 < d4
        if p12_straddles_p34 and p34_straddles_p12:
            return True

        return d1 == 0 and Segment.on_segment(*p341) \
            or d2 == 0 and Segment.on_segment(*p342) \
            or d3 == 0 and Segment.on_segment(*p123) \
            or d4 == 0 and Segment.on_segment(*p124)

    @staticmethod
    def direction(i: Coords, j: Coords, k: Coords) -> np.ndarray:
        return np.cross(k - i, j - i)

    @staticmethod
    def on_segment(seg1: Coords, seg2: Coords, point: Coords) -> bool:
        """ Определяет, принадлежит ли точка, лежащая на прямой, отрезку, лежащему на этой же прямой.

        :param seg1: Один из концов отрезка
        :param seg2: второй конец отрезка
        :param point: точка
        :return: True, если точка принадлежит отрезку, иначе False
        """
        return min(seg1.x, seg2.x) <= point.x <= max(seg1.x, seg2.x) \
            and min(seg1.y, seg2.y) <= point.y <= max(seg1.y, seg2.y)

    def distance_vector(self, pt: Coords):
        return (self._start - pt) - np.cross(self._start - pt, self.director) * self.director
