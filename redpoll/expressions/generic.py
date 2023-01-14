__all__ = ['ProgramExpr', 'BinaryExpr']

from .expression import Expr
from .blocks import ObjectBlockExpr, ToolBlockExpr, ProcessingBlockExpr
from .visitor import ExpressionVisitor
from ..types import OpType


class ProgramExpr(Expr):
    def __init__(self, o: ObjectBlockExpr = None, t: ToolBlockExpr = None, p: ProcessingBlockExpr = None) -> None:
        super().__init__()
        self.objects = o
        self.tools = t
        self.processing = p

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_program(self)


class BinaryExpr(Expr):
    # the following type hints introduce circular references and other problems
    # left: 'BinaryExpr' | EventExpr | ProcessingIdExpr | None
    # right: 'BinaryExpr' | EventExpr | ProcessingIdExpr | None

    def __init__(self, left=None, op: OpType = None, right=None) -> None:
        super().__init__()
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
