import pytest

from videoanalytics.algorithms.circles import segment_circle_intersection_points, line_circle_intersection_points, \
    on_arc
from videoanalytics.analytics.declarable.tools import Segment, Arc
from videoanalytics.models import Coords

c = Coords(7, 7), 3
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


@pytest.mark.parametrize("segment,circle,expected", [(s, c, e) for (s, e) in zip(segments, output_segments)])
def test_segment_circle_intersection_points(segment, circle, expected):
    assert segment_circle_intersection_points(segment, *circle) == expected


output_lines = [
    set(),
    {Coords(4, 7), Coords(7, 10)},
    {Coords(7, 4), Coords(7, 10)},
    {Coords(10, 7)}
]


@pytest.mark.parametrize("segment,circle,expected", [(s, c, e) for (s, e) in zip(segments, output_lines)])
def test_line_circle_intersection_points(segment, circle, expected):
    assert line_circle_intersection_points(segment, *circle) == expected


arcs = [
    Arc(Coords(4, 4), 4, 0, 180),
    Arc(Coords(4, 4), 4, 180, 0),
    Arc(Coords(4, 4), 4, 90, 270),
    Arc(Coords(4, 4), 4, 270, 90),
    Arc(Coords(4, 4), 4, 100, 260),
    Arc(Coords(4, 4), 4, 280, 80),
    # todo add 45-225 and the reverse
    # Arc(Coords(4, 4), 4, 0, 90),
    # Arc(Coords(4, 4), 4, 90, 180),
    # Arc(Coords(4, 4), 4, 180, 270),
    # Arc(Coords(4, 4), 4, 270, 360),
]

points_on_arcs = [
    [Coords(8, 4), Coords(0, 4), Coords(4, 0), Coords(5, 0)],
    [Coords(8, 4), Coords(0, 4), Coords(4, 8), Coords(3, 8)],
    [Coords(4, 0), Coords(4, 8), Coords(0, 4), Coords(0, 3)],
    [Coords(4, 0), Coords(4, 8), Coords(8, 4), Coords(8, 5)],
    [Coords(3, 0), Coords(0, 4), Coords(3, 8)],
    [Coords(8, 4), Coords(5, 0), Coords(5, 8)],
    # [Coords(5, 4), ],
    # [Coords(5, 4), ],

]

points_not_on_arcs = [
    [Coords(4, 8)],
    [Coords(4, 0)],
    [Coords(8, 4)],
    [Coords(0, 4)],
    [Coords(4, 0), Coords(4, 8)],
    [Coords(4, 0), Coords(4, 8)],
    # [],
    # [],
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
