from redpoll.expressions import ExpressionVisitor
from redpoll.expressions.atomics.coordsexpr import CoordsExpr
from redpoll.expressions.tools.toolexpr import ToolExpr
from redpoll.resources import keywords as kw


# noinspection PyTypeChecker
class SegmentExpr(ToolExpr):
    @property
    def start(self) -> CoordsExpr:
        return self.params[kw.FROM]

    @property
    def end(self) -> CoordsExpr:
        return self.params[kw.TO]

    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_segment(self)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, SegmentExpr):
            return self.start == o.start and self.end == o.end \
                   or self.start == o.end and self.end == o.start

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __hash__(self) -> int:
        return hash((self.start, self.end))

    def __repr__(self) -> str:
        return f"SegmentExpr({self.start}, {self.end})"
