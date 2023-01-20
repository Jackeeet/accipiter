from redpoll.expressions import ExpressionVisitor
from redpoll.expressions.atomics import AtomicExpr
from redpoll.types import DataType


class IntExpr(AtomicExpr):
    def __init__(self, value: int) -> None:
        assert isinstance(value, int)
        super().__init__(value)

    @property
    def type(self) -> DataType:
        return DataType.INT

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_int(self)
