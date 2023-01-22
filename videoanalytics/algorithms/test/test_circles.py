import pytest

from videoanalytics.algorithms.circles import segment_circle_intersection_points, line_circle_intersection_points
from videoanalytics.analytics.declarable.tools import Segment
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


def test_on_arc():
    assert False


def test_segment_arc_intersect():
    assert False
