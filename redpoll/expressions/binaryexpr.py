from typing import Self

from redpoll.expressions import Expr, ExpressionVisitor
from redpoll.expressions.declarable import EventExpr
from redpoll.expressions.atomics import SideExpr
from redpoll.types import OpType


class BinaryExpr(Expr):
    left: Self | EventExpr | SideExpr
    right: Self | EventExpr | SideExpr

    def __init__(self, line: int, pos: int, left=None, op: OpType = None, right=None) -> None:
        super().__init__(line, pos)
        self.left = left
        self.op = op
        self.right = right

    def __eq__(self, other):
        return self.left == other.left and \
            self.op == other.op and \
            self.right == other.right

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"BinaryExpr({self.left}, {self.op}, {self.right})"

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_binary(self)

    @staticmethod
    def from_list(items: list[Expr]) -> Expr:
        if not items:
            raise ValueError("empty list")

        left = items[0]
        for item in items[1:]:
            right = item
            left = BinaryExpr(left, OpType.OR, right)
        return left
