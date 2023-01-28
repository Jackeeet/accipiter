from redpoll.expressions import Expr, ExpressionVisitor
from redpoll.types import OpType


class BinaryExpr(Expr):
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
