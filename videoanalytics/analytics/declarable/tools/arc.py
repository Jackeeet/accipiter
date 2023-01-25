import math

import cv2
import numpy as np

from videoanalytics.analytics.declarable.tools.abstract import Component
from videoanalytics.analytics.declarable.tools.interfaces import Intersectable
from videoanalytics.analytics.declarable.tools.segment import Segment
from videoanalytics.models import Coords


class Arc(Component, Intersectable):
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
        """  Нормализованная дуга с теми же параметрами, что и исходная.

        :return: Дуга с центром в точке (0,0)
        """
        return Arc(Coords(0, 0), self.radius, self.start_angle, self.end_angle,
                   self.colour, self.thickness)

    @property
    def complement(self) -> 'Arc':
        """ Дуга, дополняющая исходную до окружности.

        :return: Дополняющая дуга
        """
        return Arc(self.center, self.radius, self.end_angle, self.start_angle)

    @property
    def is_minor(self) -> bool:
        """ Определяет, является ли дуга меньшей дугой окружности.

        :return: True, если дуга меньше 180 градусов, иначе False
        """
        return self.angle < 180

    @property
    def is_major(self) -> bool:
        """ Определяет, является ли дуга большей дугой окружности.

        :return: True, если дуга больше 180 градусов, иначе False
        """
        return self.angle > 180

    @property
    def is_semicircular(self) -> bool:
        """ Определяет, является ли дуга полуокружностью.

        :return: True, если дуга - полуокружность, иначе False
        """
        return self.angle == 180

    def intersects(self, segment) -> bool:
        return Arc.segment_arc_intersect(segment, self)

    def draw_on(self, image) -> None:
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

    @staticmethod
    def segment_arc_intersect(segment: Segment, arc: 'Arc') -> bool:
        points = Arc.segment_circle_intersection_points(segment, arc.center, arc.radius)
        return any([Arc.on_arc(point, arc) for point in points])

    @staticmethod
    def on_arc(point: Coords, arc: 'Arc') -> bool:
        if point == arc.start or point == arc.end:
            return True

        if arc.is_semicircular:
            return Arc.on_semicircular(point, arc)

        minor_arc = arc if arc.is_minor else arc.complement
        on_minor = Arc.on_minor_arc(point, minor_arc)
        return on_minor if arc.is_minor else not on_minor

    @staticmethod
    def on_minor_arc(point: Coords, arc: 'Arc') -> bool:
        if not arc.is_minor:
            raise ValueError  # todo add message

        sx, sy, ex, ey = Arc.end_signs(arc)
        zero_count = [sx, sy, ex, ey].count(0)
        in_0_x, in_0_y, in_x, in_y, in_x_radius, in_y_radius = Arc.arc_bounds(point, arc)
        if sx == ex:
            return Arc.on_vertical_half_arc(sx, sy, ey, in_x, in_y, in_x_radius, in_0_x)
        if sy == ey:
            return Arc.on_horizontal_half_arc(sx, sy, ex, in_x, in_y, in_y_radius, in_0_y)
        if zero_count == 1:
            # 90 < кол-во градусов < 180, один конец на оси
            return Arc.on_quarter_end(sx, sy, ex, ey, in_x, in_y, in_x_radius, in_y_radius, in_0_x, in_0_y)
        if zero_count == 2:
            # ровно 90 градусов (случаи со 180 градусами покрываются раньше)
            return Arc.on_quarter_arc(sx, sy, in_0_x, in_0_y, in_x_radius, in_y_radius)

        return Arc.on_opposite_quarters_arc(sx, sy, in_x_radius, in_y_radius, in_0_x, in_0_y)

    @staticmethod
    def on_quarter_end(sx, sy, ex, ey, in_x, in_y, in_x_radius, in_y_radius, in_0_x, in_0_y) -> bool:
        if sy == 0 or ey == 0:
            return in_x and (in_0_y if sx > 0 else in_y_radius)
        if sx == 0 or ex == 0:
            return (in_0_x if sy < 0 else in_x_radius) and in_y
        raise NotImplementedError("unreachable")

    @staticmethod
    def on_horizontal_half_arc(sx, sy, ex, in_x, in_y, in_y_radius, in_0_y) -> bool:
        if sx == 0 or ex == 0:
            # концы дуги в одной четверти
            return in_x and in_y

        if sy < 0:
            # концы дуги в верхней половине
            return in_x and in_0_y

        if sy > 0:
            # концы дуги в нижней половине
            return in_x and in_y_radius

        raise NotImplementedError("unreachable")

    @staticmethod
    def on_vertical_half_arc(sx, sy, ey, in_x, in_y, in_x_radius, in_0_x) -> bool:
        if sy == ey or sy == 0 or ey == 0:
            # концы дуги в одной четверти
            return in_x and in_y

        if sx < 0:
            # концы дуги в левой половине
            return in_0_x and in_y

        if sx > 0:
            # концы дуги в правой половине
            return in_x_radius and in_y

        raise NotImplementedError("unreachable")

    @staticmethod
    def on_opposite_quarters_arc(sx, sy, in_x_radius, in_y_radius, in_0_x, in_0_y) -> bool:
        in_x = in_0_x if sy < 0 else in_x_radius
        in_y = in_0_y if sx > 0 else in_y_radius
        return in_x and in_y

    @staticmethod
    def on_quarter_arc(sx, sy, in_zero_x, in_zero_y, in_x_radius, in_y_radius) -> bool:
        # оба конца дуги на краях одной четверти
        if sx == 0:
            return (in_zero_x and in_zero_y) if sy < 0 else (in_x_radius and in_y_radius)
        if sy == 0:
            return (in_zero_x and in_y_radius) if sx < 0 else (in_x_radius and in_zero_y)

        raise NotImplementedError("unreachable")

    @staticmethod
    def on_semicircular(point: Coords, arc: 'Arc') -> bool:
        if not arc.is_semicircular:
            raise ValueError  # todo add error message

        sx, sy, _, _ = Arc.end_signs(arc)
        in_0_x, in_0_y, _, _, in_x_radius, in_y_radius = Arc.arc_bounds(point, arc)

        if sx == 0:
            # дуга в левой/правой половине
            return in_0_x if sy < 0 else in_x_radius
        if sy == 0:
            # дуга в нижней/верхней половине
            return in_0_y if sx > 0 else in_y_radius

        # дуга во 2 или в 3 четверти
        split_at_left_half = sy < 0 < sx or sx < 0 and sy < 0
        split_degrees = 180 if split_at_left_half else 0
        first = Arc(arc.center, arc.radius, arc.start_angle, split_degrees)
        second = Arc(arc.center, arc.radius, split_degrees, arc.end_angle)
        return Arc.on_arc(point, first) or Arc.on_arc(point, second)

    @staticmethod
    def end_signs(arc: 'Arc') -> np.ndarray:
        norm_arc = arc.normalized
        return np.sign([norm_arc.start.x, norm_arc.start.y, norm_arc.end.x, norm_arc.end.y])

    @staticmethod
    def arc_bounds(point: Coords, arc: 'Arc') -> list[bool]:
        min_x = min(arc.start.x, arc.end.x)
        min_y = min(arc.start.y, arc.end.y)
        max_x = max(arc.start.x, arc.end.x)
        max_y = max(arc.start.y, arc.end.y)

        in_0_x = 0 <= point.x <= max_x
        in_0_y = 0 <= point.y <= max_y
        in_x = min_x <= point.x <= max_x
        in_y = min_y <= point.y <= max_y
        in_x_radius = min_x <= point.x <= arc.center.x + arc.radius
        in_y_radius = min_y <= point.y <= arc.center.y + arc.radius
        return [in_0_x, in_0_y, in_x, in_y, in_x_radius, in_y_radius]

    @staticmethod
    def segment_circle_intersection_points(segment, centre: Coords, radius: int) -> set[Coords]:
        line_intersection_points = Arc.line_circle_intersection_points(segment, centre, radius)
        return {
            point for point in line_intersection_points
            if Segment.on_segment(segment.start, segment.end, point)
        }

    @staticmethod
    def line_circle_intersection_points(segment, centre: Coords, radius: int) -> set[Coords]:
        seg_vec = segment.end - segment.start
        centre_dist = segment.start - centre

        a = np.dot(seg_vec, seg_vec)
        b = 2 * np.dot(centre_dist, seg_vec)
        c = np.dot(centre_dist, centre_dist) - (radius ** 2)

        roots = np.roots([a, b, c])
        roots = roots[np.isclose(roots.imag, 0)]

        return {
            Coords(
                round(segment.start.x + root * seg_vec[0]),
                round(segment.start.y + root * seg_vec[1])
            ) for root in roots
        }
