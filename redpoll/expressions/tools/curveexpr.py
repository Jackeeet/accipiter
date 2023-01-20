from redpoll.expressions import ExpressionVisitor
from redpoll.expressions.atomics.coordsexpr import CoordsExpr
from redpoll.expressions.tools.toolexpr import ToolExpr
from redpoll.resources import keywords as kw


# noinspection PyTypeChecker
class CurveExpr(ToolExpr):
    # this should calculate the start point
    # from the center, radius and the start angle
    @property
    def start(self) -> CoordsExpr:
        return self.params["asdf"]

    @property
    def end(self) -> CoordsExpr:
        return self.params["asdf"]

    @property
    def radius(self) -> int:
        return self.params["радиус"]

    @property
    def center(self) -> CoordsExpr:
        return self.params[kw.CENTER]

    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_curve(self)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, CurveExpr):
            # the last two checks might be unnecessary,
            # but I don't know basic geometry,
            # so I'm going to leave this as it is
            return self.start == o.start and self.end == o.end \
                   and self.center == o.center and self.radius == o.radius

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __hash__(self) -> int:
        return hash((self.start, self.end, self.center, self.radius))
