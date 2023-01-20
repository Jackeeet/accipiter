from redpoll.expressions import ExpressionVisitor
from redpoll.expressions.atomics.coordsexpr import CoordsExpr
from redpoll.expressions.tools.toolexpr import ToolExpr
from redpoll.resources import keywords as kw


class PointExpr(ToolExpr):
    @property
    def coords(self) -> CoordsExpr:
        # noinspection PyTypeChecker
        return self.params[kw.POINT]

    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_point(self)
