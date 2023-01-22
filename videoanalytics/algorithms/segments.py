import numpy as np

from videoanalytics.analytics.declarable.tools import Segment
from videoanalytics.models import Coords


def segments_intersect(s1: Segment, s2: Segment) -> bool:
    """ Определяет, пересекаются ли два отрезка.

    :param s1: первый отрезок
    :param s2: второй отрезок
    :return: True, если отрезки пересекаются, иначе False
    """
    p341 = (s2.start, s2.end, s1.start)
    p342 = (s2.start, s2.end, s1.end)
    p123 = (s1.start, s1.end, s2.start)
    p124 = (s1.start, s1.end, s2.end)

    d1 = direction(*p341)
    d2 = direction(*p342)
    d3 = direction(*p123)
    d4 = direction(*p124)

    p12_straddles_p34 = d1 > 0 > d2 or d1 < 0 < d2
    p34_straddles_p12 = d3 > 0 > d4 or d3 < 0 < d4
    if p12_straddles_p34 and p34_straddles_p12:
        return True

    return d1 == 0 and on_segment(*p341) or d2 == 0 and on_segment(*p342) or \
           d3 == 0 and on_segment(*p123) or d4 == 0 and on_segment(*p124)


def direction(i: Coords, j: Coords, k: Coords) -> np.ndarray:
    return np.cross(k - i, j - i)


def on_segment(seg1: Coords, seg2: Coords, point: Coords) -> bool:
    """ Определяет, принадлежит ли точка, лежащая на прямой, отрезку, лежащему на этой же прямой.

    :param seg1: один из концов отрезка
    :param seg2: второй конец отрезка
    :param point: точка
    :return: True, если точка принадлежит отрезку, иначе False
    """
    return min(seg1.x, seg2.x) <= point.x <= max(seg1.x, seg2.x) \
           and min(seg1.y, seg2.y) <= point.y <= max(seg1.y, seg2.y)
