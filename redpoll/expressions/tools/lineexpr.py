from redpoll.expressions import ExpressionVisitor
from redpoll.expressions.tools.toolexpr import ToolExpr


class LineExpr(ToolExpr):
    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_line(self)
