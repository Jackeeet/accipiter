import pytest

from videoanalytics.analytics.declarable.tools import Arc
from videoanalytics.models import Coords

radius = 4
center = Coords(radius, radius)

arcs = [
    Arc(center, radius, 0, 180),
    Arc(center, radius, 180, 0),
    Arc(center, radius, 90, 270),
    Arc(center, radius, 270, 90),
    Arc(center, radius, 75, 255),
    Arc(center, radius, 255, 75),
    Arc(center, radius, 45, 225),
    Arc(center, radius, 225, 45),
]

starts = [
    Coords(8, 4),
    Coords(0, 4),
    Coords(4, 0),
    Coords(4, 8),
    Coords(5, 0),
    Coords(3, 8),
    Coords(7, 1),
    Coords(1, 7)
]

ends = [
    Coords(0, 4),
    Coords(8, 4),
    Coords(4, 8),
    Coords(4, 0),
    Coords(3, 8),
    Coords(5, 0),
    Coords(1, 7),
    Coords(7, 1)
]


@pytest.mark.parametrize("arc, expected", [(a, e) for (a, e) in zip(arcs, starts)])
def test_start(arc, expected):
    assert arc.start == expected


@pytest.mark.parametrize("arc, expected", [(a, e) for (a, e) in zip(arcs, ends)])
def test_end(arc, expected):
    assert arc.end == expected


arcs_to_norm = [
    Arc(Coords(0, 0), 1, 90, 270),
    Arc(Coords(-1, 3), 2, 180, 0),
    Arc(Coords(-4, -6), 3, 270, 90),
    Arc(Coords(8, 4), 4, 0, 180),
    Arc(Coords(6, -1), 5, 75, 255)
]


@pytest.mark.parametrize("arc", arcs_to_norm)
def test_normalized(arc):
    assert arc.normalized.center == Coords(0, 0) \
           and arc.normalized.radius == arc.radius \
           and arc.normalized.start_angle == arc.start_angle \
           and arc.normalized.end_angle == arc.end_angle
