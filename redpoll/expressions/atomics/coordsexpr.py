from redpoll.expressions import ExpressionVisitor
from redpoll.expressions.atomics import AtomicExpr
from redpoll.types import DataType


class CoordsExpr(AtomicExpr):
    def __init__(self, value: tuple[int, int]) -> None:
        assert isinstance(value, tuple)
        assert len(value) == 2
        super().__init__(value)

    @property
    def x(self):
        return self.value[0]

    @property
    def y(self):
        return self.value[1]

    @property
    def type(self) -> DataType:
        return DataType.COORDS

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_coords(self)
