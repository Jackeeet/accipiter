from redpoll.expressions import ExpressionVisitor
from redpoll.expressions.atomics import AtomicExpr
from redpoll.types import DataType


class FloatExpr(AtomicExpr):
    def __init__(self, value: float) -> None:
        assert isinstance(value, float)
        super().__init__(value)

    @property
    def type(self) -> DataType:
        return DataType.FLOAT

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_float(self)
