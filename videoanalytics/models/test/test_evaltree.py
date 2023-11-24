from .mock_event import MockEvent
from videoanalytics.models import EvalTree, Side, SideValue, TrackedState
from videoanalytics.models.boolean import Boolean


def test_evaluates_single_bool():
    tree = EvalTree(op_or_val=MockEvent(True))
    assert tree.evaluate()


def test_evaluates_bool_chains():
    tree = EvalTree(
        MockEvent(True),
        "op_and",
        EvalTree(
            MockEvent(False),
            "op_or",
            MockEvent(True)
        )
    )
    assert tree.evaluate()


def test_evaluates_single_side():
    tree = EvalTree(op_or_val=Side(SideValue.LEFT))
    assert tree.evaluate() == TrackedState.CROSSING_LEFT


def test_evaluates_side_conjunctions():
    tree = EvalTree(
        Side(SideValue.LEFT),
        "op_and",
        Side(SideValue.RIGHT)
    )

    expected = TrackedState.CROSSING_LEFT | TrackedState.CROSSING_RIGHT
    assert tree.evaluate() == expected


def test_evaluates_side_disjunctions():
    tree = EvalTree(
        Side(SideValue.LEFT),
        "op_or",
        Side(SideValue.RIGHT)
    )

    expected = TrackedState.CROSSING_LEFT | TrackedState.CROSSING_RIGHT
    assert tree.evaluate() == expected


def test_evaluates_all_sides():
    tree = EvalTree(
        Side(SideValue.LEFT), 'op_or', EvalTree(
            Side(SideValue.RIGHT), 'op_or', EvalTree(
                Side(SideValue.TOP), 'op_or', Side(SideValue.BOTTOM)
            )
        )
    )

    expected = TrackedState.CROSSING_LEFT | TrackedState.CROSSING_RIGHT \
               | TrackedState.CROSSING_TOP | TrackedState.CROSSING_BOTTOM
    assert tree.evaluate() == expected


sides_crossing = {SideValue.RIGHT: Boolean(True), SideValue.LEFT: Boolean(False)}


def test_fmaps_single_side():
    fmapped = EvalTree(op_or_val=Side(SideValue.LEFT)) \
        .fmap(lambda side: sides_crossing[side.value])
    assert not fmapped.evaluate()


def test_fmaps_side_conjunction_chains():
    tree = EvalTree(
        Side(SideValue.LEFT),
        "op_and",
        Side(SideValue.RIGHT)
    )
    fmapped = tree.fmap(lambda side: sides_crossing[side.value])
    assert not fmapped.evaluate()


def test_fmaps_side_disjunction_chains():
    tree = EvalTree(
        Side(SideValue.LEFT),
        "op_or",
        Side(SideValue.RIGHT)
    )
    fmapped = tree.fmap(lambda side: sides_crossing[side.value])
    assert fmapped.evaluate()
