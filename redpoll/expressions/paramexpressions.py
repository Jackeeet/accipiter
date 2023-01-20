__all__ = ['ParamsExpr', 'AtomicExpr', 'ToolPartsExpr']

from abc import ABC

from redpoll.expressions.expression import Expr
from redpoll.expressions.visitor import ExpressionVisitor
from redpoll.types import DataType


class ParamsExpr(Expr, ABC):
    pass


class AtomicExpr(ParamsExpr):
    _allowed_types: set[DataType] = {
        DataType.COLOUR, DataType.COORDS,
        DataType.FLOAT, DataType.INT,
        DataType.STRING
    }

    def __init__(self, value: tuple[int, int, int] | tuple[int, int] | int | str, atomic_type: DataType) -> None:
        super().__init__()
        self.value = f"'{value}'" if isinstance(value, str) else value
        if atomic_type not in AtomicExpr._allowed_types:
            raise ValueError("Unsupported atomic type")
        self.type = atomic_type

    def __eq__(self, o: object) -> bool:
        if isinstance(o, AtomicExpr):
            return self.value == o.value and self.type == o.type
        return False

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __repr__(self) -> str:
        return f"AtomicExpr({self.value}, {self.type})"

    def __hash__(self):
        return self.value.__hash__()

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_atomic(self)


class ToolPartsExpr(ParamsExpr):
    # array: list[ToolExpr | ToolIdExpr]

    def __init__(self, arr) -> None:
        super().__init__()
        self.parts = arr

    def __eq__(self, other):
        return self.parts == other.parts

    def __ne__(self, other):
        return self.parts != other.parts

    def __repr__(self):
        return f"ToolPartsExpr({self.parts})"

    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_tool_parts(self)
