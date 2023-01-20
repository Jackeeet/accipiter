__all__ = ['ParamsExpr', 'ToolPartsExpr']

from abc import ABC

from redpoll.expressions.expr import Expr
from redpoll.expressions.visitor import ExpressionVisitor


class ParamsExpr(Expr, ABC):
    pass


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
