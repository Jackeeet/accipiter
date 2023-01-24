import pytest

from videoanalytics.algorithms.arcs import segment_circle_intersection_points, line_circle_intersection_points, \
    on_arc
from videoanalytics.analytics.declarable.tools import Segment, Arc
from videoanalytics.models import Coords

circle_center = Coords(7, 7), 3
segments = [
    Segment(Coords(1, 3), Coords(3, 1)),
    Segment(Coords(2, 5), Coords(8, 11)),
    Segment(Coords(7, 1), Coords(7, 4)),
    Segment(Coords(10, 5), Coords(10, 9)),
]

output_segments = [
    set(),
    {Coords(4, 7), Coords(7, 10)},
    {Coords(7, 4)},
    {Coords(10, 7)}
]


@pytest.mark.parametrize("segment,circle,expected",
                         [(s, circle_center, e) for (s, e) in zip(segments, output_segments)])
def test_segment_circle_intersection_points(segment, circle, expected):
    assert segment_circle_intersection_points(segment, *circle) == expected


output_lines = [
    set(),
    {Coords(4, 7), Coords(7, 10)},
    {Coords(7, 4), Coords(7, 10)},
    {Coords(10, 7)}
]


@pytest.mark.parametrize("segment,circle,expected", [(s, circle_center, e) for (s, e) in zip(segments, output_lines)])
def test_line_circle_intersection_points(segment, circle, expected):
    assert line_circle_intersection_points(segment, *circle) == expected


c = Coords(4, 4)
r = 4

left = Coords(0, 4)
right = Coords(8, 4)
top = Coords(4, 0)
bottom = Coords(4, 8)

bottom_left = Coords(1, 7)
top_left = Coords(1, 1)
bottom_right = Coords(7, 7)
top_right = Coords(7, 1)

semicircular = [
    # vertical/horizontal
    Arc(c, r, 0, 180),
    Arc(c, r, 180, 0),
    Arc(c, r, 90, 270),
    Arc(c, r, 270, 90),
    # diagonal
    Arc(c, r, 45, 225),
    Arc(c, r, 225, 45),
    Arc(c, r, 135, 315),
    Arc(c, r, 315, 135),
]

points_on_semis = [
    # vertical/horizontal
    [right, left, top, Coords(5, 0)],
    [right, left, bottom, Coords(3, 8)],
    [top, bottom, left, Coords(0, 3)],
    [top, bottom, right, Coords(8, 5)],
    # diagonal
    [top_right, bottom_left, top_left, Coords(3, 0)],
    [bottom_left, top_right, bottom_right, Coords(8, 5)],
    [top_left, bottom_right, bottom_left],
    [bottom_right, top_left, top_right],
]

points_not_on_semis = [
    # vertical/horizontal
    [bottom], [top], [right], [left],
    # diagonal
    [right], [top], [top], [left],
]

quarters = [
    Arc(c, r, 0, 90),
    Arc(c, r, 90, 180),
    Arc(c, r, 180, 270),
    Arc(c, r, 270, 360),

    Arc(c, r, 90, 0),
    Arc(c, r, 180, 90),
    Arc(c, r, 270, 180),
    Arc(c, r, 360, 270),

    Arc(c, r, 45, 135),
    Arc(c, r, 135, 225),
    Arc(c, r, 225, 315),
    Arc(c, r, 315, 45),

    Arc(c, r, 135, 45),
    Arc(c, r, 225, 135),
    Arc(c, r, 315, 225),
    Arc(c, r, 45, 315),
]

points_on_quarters = [
    [right, top, top_right],
    [top, left, top_left],
    [left, bottom, bottom_left],
    [bottom, right, Coords(7, 4)],

    [top, left, bottom, right],
    [top, left, bottom, right],
    [top, left, bottom, right],
    [top, left, bottom, right],

    [top_right, top, top_left],
    [top_left, left, bottom_left],
    [bottom_left, bottom, bottom_right],
    [bottom_right, right, top_right],

    [top_left, bottom, top_right],
    [bottom_left, right, top_left],
    [bottom_right, top, bottom_left],
    [top_right, left, bottom_right],
]

points_not_on_quarters = [
    [bottom, left], [bottom, right], [top, right], [top, left],

    [top_right], [top_left], [bottom_left], [bottom_right],

    [Coords(8, 3), Coords(0, 3)],
    [Coords(3, 0), Coords(3, 8)],
    [Coords(0, 5), Coords(8, 5)],
    [Coords(5, 8), Coords(5, 0)],

    [top], [left], [bottom], [right],
]

arcs = semicircular + quarters + [
    # 1/8
    Arc(c, r, 90, 135),
    Arc(c, r, 180, 225),
    Arc(c, r, 225, 270),
    Arc(c, r, 315, 0),
    # 7/8
    Arc(c, r, 135, 90),
    Arc(c, r, 225, 180),
    Arc(c, r, 270, 225),
    Arc(c, r, 0, 315),
    # 3/8
    Arc(c, r, 45, 180),
    Arc(c, r, 135, 270),
    Arc(c, r, 225, 0),
    Arc(c, r, 315, 90),
    Arc(c, r, 0, 135),
    Arc(c, r, 90, 225),
    Arc(c, r, 180, 315),
    Arc(c, r, 270, 45),
    # 5/8
    Arc(c, r, 180, 45),
    Arc(c, r, 270, 135),
    Arc(c, r, 0, 225),
    Arc(c, r, 90, 315),
    Arc(c, r, 135, 0),
    Arc(c, r, 225, 90),
    Arc(c, r, 315, 180),
    Arc(c, r, 45, 270),
    # sign() != 0 for all the following arcs' edges
    # vertical
    Arc(c, r, 100, 260),
    Arc(c, r, 280, 80),
    # horizontal
    Arc(c, r, 10, 170),
    Arc(c, r, 190, 350),
    # ends in same quarter
    Arc(c, r, 10, 80),
    Arc(c, r, 100, 170),
    Arc(c, r, 190, 260),
    Arc(c, r, 280, 350),
    # ends in opposite quarters
    Arc(c, r, 10, 260),
    Arc(c, r, 260, 10),
    Arc(c, r, 170, 280),
    Arc(c, r, 280, 170),
]

points_on_arcs = points_on_semis + points_on_quarters + [
    # 1/8
    [top, top_left],
    [left, bottom_left],
    [bottom_left, bottom],
    [bottom_right, right],
    # 7/8
    [top, top_left, left, bottom, right],
    [left, bottom_left, bottom, right, top],
    [bottom_left, bottom, right, top, left],
    [bottom_right, right, top, left, bottom],
    # 3/8
    [top_right, top, top_left, left],
    [top_left, left, bottom_left, bottom],
    [bottom_left, bottom, bottom_right, right],
    [bottom_right, right, top_right, top],
    [right, top_right, top, top_left],
    [top, top_left, left, bottom_left],
    [left, bottom_left, bottom, bottom_right],
    [bottom, bottom_right, right, top_right],
    # 5/8
    [left, bottom_right, top_right],
    [bottom, right, top_left],
    [right, top_left, bottom_left],
    [top, left, bottom_right],
    [top_left, bottom, right],
    [bottom_left, right, top],
    [bottom_right, top, left],
    [top_right, left, bottom],
    # vertical
    [Coords(3, 0), left, Coords(3, 8)],
    [right, Coords(5, 0), Coords(5, 8)],
    # horizontal
    [Coords(8, 3), Coords(0, 3), top],
    [Coords(8, 5), Coords(0, 5), bottom],
    # ends in same quarter
    [Coords(8, 3), top_right, Coords(5, 0)],
    [Coords(3, 0), top_left, Coords(0, 3)],
    [Coords(0, 5), bottom_left, Coords(3, 8)],
    [Coords(5, 8), bottom_right, Coords(8, 5)],
    # ends in opposite quarters
    [Coords(8, 3), top, left, Coords(3, 8)],
    [Coords(3, 8), bottom, right, Coords(8, 3)],
    [Coords(0, 3), left, bottom, Coords(5, 8)],
    [Coords(5, 8), top, right, Coords(0, 3)],
]

points_not_on_arcs = points_not_on_semis + points_not_on_quarters + [
    # 1/8
    [left, top_right],
    [top_left, bottom],
    [left, bottom_right],
    [bottom, top_right],
    # 7/8
    [Coords(3, 0)], [Coords(0, 5)], [Coords(3, 8)], [Coords(8, 5)],
    # 3/8
    [bottom_left, bottom, bottom_right, right],
    [bottom_right, right, top_right, top],
    [top_right, top, top_left, left],
    [top_left, left, bottom_left, bottom],
    [left, bottom_left, bottom, bottom_right],
    [bottom, bottom_right, right, top_right],
    [right, top_right, top, top_left],
    [top, top_left, left, bottom_left],
    # 5/8
    [top, top_left],
    [left, bottom_left],
    [bottom, bottom_right],
    [right, top_right],
    [top_right, top],
    [top_left, left],
    [bottom_left, bottom],
    [bottom_right, right],
    # vertical
    [top, bottom],
    [top, bottom],
    # horizontal
    [right, left],
    [right, left],
    # ends in same quarter
    [right, top],
    [top, left],
    [left, bottom],
    [bottom, right],
    # ends in opposite quarters
    [bottom, right],
    [top, left],
    [top, right],
    [bottom, left],
]


@pytest.mark.parametrize("points, arc", [(p, a) for (p, a) in zip(points_on_arcs, arcs)])
def test_on_arc(points, arc):
    for point in points:
        assert on_arc(point, arc)


@pytest.mark.parametrize("points, arc", [(p, a) for (p, a) in zip(points_not_on_arcs, arcs)])
def test_not_on_arc(points, arc):
    for point in points:
        assert not on_arc(point, arc)


def test_segment_arc_intersect():
    assert False
