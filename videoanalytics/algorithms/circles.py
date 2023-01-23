import numpy as np

from videoanalytics.algorithms.segments import on_segment
from videoanalytics.analytics.declarable.tools import Segment, Arc
from videoanalytics.models import Coords


def segment_arc_intersect(segment: Segment, arc: Arc) -> bool:
    points = segment_circle_intersection_points(segment, arc.center, arc.radius)
    return any([on_arc(point, arc) for point in points])


def on_arc(point: Coords, arc: Arc) -> bool:
    norm_arc = arc.normalized
    sx, sy, ex, ey = np.sign(
        [norm_arc.start.x, norm_arc.start.y, norm_arc.end.x, norm_arc.end.y]
    )

    min_x = min(arc.start.x, arc.end.x)
    min_y = min(arc.start.y, arc.end.y)
    max_x = max(arc.start.x, arc.end.x)
    max_y = max(arc.start.y, arc.end.y)

    in_zero_x = 0 <= point.x <= max_x
    in_zero_y = 0 <= point.y <= max_y
    in_x_bounds = min_x <= point.x <= max_x
    in_y_bounds = min_y <= point.y <= max_y
    in_x_radius = min_x <= point.x <= arc.center.x + arc.radius
    in_y_radius = min_y <= point.y <= arc.center.y + arc.radius

    if arc.is_semicircular and sx == 0:
        return in_zero_x if sy < 0 else in_x_radius
    if arc.is_semicircular and sy == 0:
        return in_zero_y if sx > 0 else in_y_radius

    if sx == ex:
        # концы дуги в одной четверти
        if sy == ey:
            in_arc = in_x_bounds and in_y_bounds
        # концы дуги в левой половине
        elif sx < 0:
            in_arc = in_zero_x and in_y_bounds
        # концы дуги в правой половине
        elif sx > 0:
            in_arc = in_x_radius and in_y_bounds
        else:  # sx == 0 and ex == 0
            raise NotImplementedError("unreachable: sx == ex, sx == 0")
    elif sy == ey:
        # концы дуги в нижней половине
        if sx < 0:
            in_arc = in_x_bounds and in_y_radius
        # концы дуги в верхней половине
        elif sx > 0:
            in_arc = in_x_bounds and in_zero_y
        else:
            raise NotImplementedError("unreachable: sy == ey, sx == 0")
    # концы дуги в противоположных четвертях
    else:
        in_x = in_zero_x if sy < 0 else in_x_radius
        in_y = in_zero_y if sx < 0 else in_y_radius
        in_arc = in_x and in_y

    # принадлежность точки к дуге рассчитывается по меньшей из дуг окружности,
    # если дуга - большая, результат инвертируется
    return in_arc if arc.is_minor else not in_arc


def segment_circle_intersection_points(segment: Segment, centre: Coords, radius: int) -> set[Coords]:
    line_intersection_points = line_circle_intersection_points(segment, centre, radius)
    return {
        point for point in line_intersection_points
        if on_segment(segment.start, segment.end, point)
    }


def line_circle_intersection_points(segment: Segment, centre: Coords, radius: int) -> set[Coords]:
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
