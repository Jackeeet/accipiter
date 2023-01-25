import math

from redpoll.expressions import ExpressionVisitor
from redpoll.expressions.atomics.coordsexpr import CoordsExpr
from redpoll.expressions.tools.toolexpr import ToolExpr
from redpoll.resources import keywords as kw


class ArcExpr(ToolExpr):
    @property
    def start(self) -> CoordsExpr:
        return self.coords_from_degrees(self.params[kw.ANGLE_FROM].value)

    @property
    def end(self) -> CoordsExpr:
        return self.coords_from_degrees(self.params[kw.ANGLE_TO].value)

    @property
    def radius(self) -> int:
        return self.params[kw.RADIUS].value

    @property
    def center(self) -> CoordsExpr:
        return self.params[kw.CENTER]

    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_arc(self)

    def coords_from_degrees(self, deg_angle: int) -> CoordsExpr:
        rad_angle = math.radians(deg_angle)
        return CoordsExpr((
            self.center.x + round(self.radius * math.cos(rad_angle)),
            self.center.y + round(self.radius * -math.sin(rad_angle))
        ))

    def __eq__(self, o: object) -> bool:
        if isinstance(o, ArcExpr):
            # the last two checks might be unnecessary,
            # but I don't know basic geometry,
            # so I'm going to leave this as it is
            return self.start == o.start and self.end == o.end \
                   and self.center == o.center and self.radius == o.radius

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __hash__(self) -> int:
        return hash((self.start, self.end, self.center, self.radius))
