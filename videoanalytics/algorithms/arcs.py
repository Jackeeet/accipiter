import numpy as np

from videoanalytics.algorithms.segments import on_segment
from videoanalytics.analytics.declarable.tools import Segment, Arc
from videoanalytics.models import Coords


def segment_arc_intersect(segment: Segment, arc: Arc) -> bool:
    points = segment_circle_intersection_points(segment, arc.center, arc.radius)
    return any([on_arc(point, arc) for point in points])


def on_arc(point: Coords, arc: Arc) -> bool:
    if arc.is_semicircular:
        return on_semicircular(point, arc)

    sx, sy, ex, ey = end_signs(arc)
    in_zero_x, in_zero_y, in_x_bounds, \
        in_y_bounds, in_x_radius, in_y_radius = arc_bounds(point, arc)

    if sx == ex:
        in_arc = on_vertical_half_arc(ey, in_x_bounds, in_x_radius, in_y_bounds, in_zero_x, sx, sy)
    elif sy == ey:
        in_arc = on_horizontal_half_arc(ex, in_x_bounds, in_y_bounds, in_y_radius, in_zero_y, sx, sy)
    elif sx == 0 or sy == 0 or ex == 0 or ey == 0:
        in_arc = on_quarter_arc()
    else:
        in_arc = on_opposite_quarters_arc(in_x_radius, in_y_radius, in_zero_x, in_zero_y, sx, sy)

    # принадлежность точки к дуге рассчитывается по меньшей из дуг окружности,
    # если дуга - большая, результат инвертируется
    return in_arc if arc.is_minor else not in_arc


def on_horizontal_half_arc(ex, in_x_bounds, in_y_bounds, in_y_radius, in_zero_y, sx, sy) -> bool:
    if sx == 0 or ex == 0:
        # концы дуги в одной четверти
        return in_x_bounds and in_y_bounds

    if sy < 0:
        # концы дуги в верхней половине
        return in_x_bounds and in_zero_y

    if sy > 0:
        # концы дуги в нижней половине
        return in_x_bounds and in_y_radius

    raise NotImplementedError("unreachable")


def on_vertical_half_arc(ey, in_x_bounds, in_x_radius, in_y_bounds, in_zero_x, sx, sy) -> bool:
    if sy == ey or sy == 0 or ey == 0:
        # концы дуги в одной четверти
        return in_x_bounds and in_y_bounds

    if sx < 0:
        # концы дуги в левой половине
        return in_zero_x and in_y_bounds

    if sx > 0:
        # концы дуги в правой половине
        return in_x_radius and in_y_bounds

    raise NotImplementedError("unreachable")


def on_opposite_quarters_arc(in_x_radius, in_y_radius, in_zero_x, in_zero_y, sx, sy) -> bool:
    in_x = in_zero_x if sy < 0 else in_x_radius
    in_y = in_zero_y if sx < 0 else in_y_radius
    return in_x and in_y


def on_quarter_arc() -> bool:
    # оба конца дуги на краях одной четверти
    raise NotImplementedError


def on_semicircular(point: Coords, arc: Arc) -> bool:
    if not arc.is_semicircular:
        raise ValueError  # todo add error message

    sx, sy, _, _ = end_signs(arc)
    in_zero_x, in_zero_y, in_x_bounds, \
        in_y_bounds, in_x_radius, in_y_radius = arc_bounds(point, arc)

    if sx == 0:
        # дуга в левой/правой половине
        return in_zero_x if sy < 0 else in_x_radius
    if sy == 0:
        # дуга в нижней/верхней половине
        return in_zero_y if sx > 0 else in_y_radius
    if sy < 0 < sx:
        # начало в 1 четверти, дуга во 2 четверти
        raise NotImplementedError
    if sx < 0 and sy < 0:
        # дуга в 3 четверти
        raise NotImplementedError
    if sx < 0 < sy:
        # дуга в 4 четверти
        raise NotImplementedError
    if sx > 0 and sy > 0:
        # дуга в 1 четверти
        raise NotImplementedError


def end_signs(arc: Arc) -> np.ndarray:
    norm_arc = arc.normalized
    return np.sign([norm_arc.start.x, norm_arc.start.y, norm_arc.end.x, norm_arc.end.y])


def arc_bounds(point: Coords, arc: Arc) -> list[bool]:
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
    return [in_zero_x, in_zero_y, in_x_bounds, in_y_bounds, in_x_radius, in_y_radius]


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
