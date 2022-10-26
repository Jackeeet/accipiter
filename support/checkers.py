import numpy as np

from support.primitives import Point, Segment


def segments_intersect(s1: Segment, s2: Segment) -> bool:
    p341 = (s2.start, s2.end, s1.start)
    p342 = (s2.start, s2.end, s1.end)
    p123 = (s1.start, s1.end, s2.start)
    p124 = (s1.start, s1.end, s2.end)

    d1 = _direction(*p341)
    d2 = _direction(*p342)
    d3 = _direction(*p123)
    d4 = _direction(*p124)

    p12_straddles_p34 = d1 > 0 and d2 < 0 or d1 < 0 and d2 > 0
    p34_straddles_p12 = d3 > 0 and d4 < 0 or d3 < 0 and d4 > 0
    if p12_straddles_p34 and p34_straddles_p12:
        return True

    return d1 == 0 and _on_segment(*p341) or d2 == 0 and _on_segment(*p342) \
        or d3 == 0 and _on_segment(*p123) or d4 == 0 and _on_segment(*p124)


def _direction(pi: Point, pj: Point, pk: Point) -> np.ndarray:
    i = np.asarray(pi)
    j = np.asarray(pj)
    k = np.asarray(pk)
    return np.cross(k - i, j - i)


def _on_segment(i: Point, j: Point, k: Point) -> bool:
    return min(i.x, j.x) <= k.x <= max(i.x, j.x) \
        and min(i.y, j.y) <= k.y <= max(i.y, j.y)
