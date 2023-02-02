from redpoll.expressions import ExpressionVisitor
from redpoll.expressions.atomics import AtomicExpr
from redpoll.types import DataType


class StringExpr(AtomicExpr):
    def __init__(self, line: int, pos: int, value: str) -> None:
        assert isinstance(value, str)
        super().__init__(line, pos, f"'{value}'")

    @property
    def type(self) -> DataType:
        return DataType.STRING

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_string(self)
