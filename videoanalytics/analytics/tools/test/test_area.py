import pytest

from videoanalytics.analytics.tools import Segment, Area
from videoanalytics.models import Coords, Box

component_lists = {
    "triangle": [
        Segment(Coords(30, 30), Coords(60, 30)),
        Segment(Coords(60, 30), Coords(45, 60)),
        Segment(Coords(45, 60), Coords(30, 30)),
    ],
    "rectangle": [
        Segment(Coords(20, 20), Coords(80, 20)),
        Segment(Coords(80, 20), Coords(80, 60)),
        Segment(Coords(80, 60), Coords(20, 60)),
        Segment(Coords(20, 60), Coords(20, 20)),
    ],
    "pentagon": [
        Segment(Coords(30, 30), Coords(40, 25)),
        Segment(Coords(40, 25), Coords(50, 27)),
        Segment(Coords(50, 27), Coords(45, 50)),
        Segment(Coords(45, 50), Coords(33, 40)),
        Segment(Coords(33, 40), Coords(30, 30)),
    ],
    "star": [
        Segment(Coords(20, 10), Coords(21, 13)),
        Segment(Coords(21, 13), Coords(24, 13)),
        Segment(Coords(24, 13), Coords(22, 15)),
        Segment(Coords(22, 15), Coords(23, 18)),
        Segment(Coords(23, 18), Coords(20, 16)),
        Segment(Coords(20, 16), Coords(17, 18)),
        Segment(Coords(17, 18), Coords(18, 15)),
        Segment(Coords(18, 15), Coords(16, 13)),
        Segment(Coords(16, 13), Coords(19, 13)),
        Segment(Coords(19, 13), Coords(20, 10)),
    ]
}

areas_convex = [
    (Area(component_lists["triangle"]), True),
    (Area(component_lists["rectangle"]), True),
    (Area(component_lists["pentagon"]), True),
    (Area(component_lists["star"]), False),
]


@pytest.mark.parametrize("area, expected", areas_convex)
def test_convex(area, expected):
    assert area.convex == expected


areas_overlapping_boxes = [
    (Area(component_lists["triangle"]), Box(Coords(40, 35), 10, 5)),
    (Area(component_lists["triangle"]), Box(Coords(30, 45), 20, 15)),
    (Area(component_lists["triangle"]), Box(Coords(40, 10), 10, 20)),
    (Area(component_lists["triangle"]), Box(Coords(60, 30), 10, 5)),
]


@pytest.mark.parametrize("area, box", areas_overlapping_boxes)
def test_overlaps(area, box):
    assert area.overlaps(box)


areas_not_overlapping_boxes = [
    (Area(component_lists["triangle"]), Box(Coords(0, 0), 10, 5)),
]


@pytest.mark.parametrize("area, box", areas_not_overlapping_boxes)
def test_does_not_overlap(area, box):
    assert not area.overlaps(box)


areas_containing_boxes = [
    (Area(component_lists["triangle"]), Box(Coords(40, 35), 10, 5)),
]


@pytest.mark.parametrize("area, box", areas_containing_boxes)
def test_contains(area, box):
    assert area.contains(box)


areas_not_containing_boxes = [
    (Area(component_lists["triangle"]), Box(Coords(0, 0), 10, 5)),
    (Area(component_lists["triangle"]), Box(Coords(30, 45), 20, 15)),
    (Area(component_lists["triangle"]), Box(Coords(40, 10), 10, 20)),
    (Area(component_lists["triangle"]), Box(Coords(60, 30), 10, 5)),
]


@pytest.mark.parametrize("area, box", areas_not_containing_boxes)
def test_does_not_contain(area, box):
    assert not area.contains(box)
