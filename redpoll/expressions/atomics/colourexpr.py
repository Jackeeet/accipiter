from redpoll.expressions import ExpressionVisitor
from redpoll.expressions.atomics import AtomicExpr
from redpoll.types import DataType


class ColourExpr(AtomicExpr):
    def __init__(self, value: tuple[int, int, int]) -> None:
        assert isinstance(value, tuple)
        assert len(value) == 3
        super().__init__(value)

    @property
    def type(self) -> DataType:
        return DataType.COLOUR

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_colour(self)
