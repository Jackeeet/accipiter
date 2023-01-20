__all__ = ['ToolExpr', 'PointExpr', 'SegmentExpr', 'CurveExpr',
           'AreaExpr', 'LineExpr', 'CounterExpr']

from abc import ABC

from redpoll.expressions import CoordsExpr
from redpoll.expressions.blockitems import BlockItemExpr
from redpoll.expressions.identifiers import ToolIdExpr
from redpoll.expressions.paramexpressions import ParamsExpr
from redpoll.expressions.visitor import ExpressionVisitor
from redpoll.types import DataType
import redpoll.resources.keywords as kw


class ToolExpr(BlockItemExpr, ABC):
    id: ToolIdExpr | None
    params: dict[str, ParamsExpr]

    def __init__(self, name: ToolIdExpr = None) -> None:
        super().__init__()
        self.id = name
        self.params = dict()

    def __eq__(self, o: object) -> bool:
        if isinstance(o, ToolExpr):
            return self.id == o.id
        return False

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    @staticmethod
    def instantiate_with_type(tool_type: DataType):
        match tool_type:
            case DataType.POINT:
                return PointExpr()
            case DataType.SEGMENT:
                return SegmentExpr()
            case DataType.CURVE:
                return CurveExpr()
            case DataType.AREA:
                return AreaExpr()
            case DataType.LINE:
                return LineExpr()
            case DataType.COUNTER:
                return CounterExpr()
            case _:
                raise ValueError("Unsupported tool type")


class PointExpr(ToolExpr):
    @property
    def coords(self) -> CoordsExpr:
        # noinspection PyTypeChecker
        return self.params[kw.POINT]

    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_point(self)


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


class AreaExpr(ToolExpr):
    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_area(self)


class LineExpr(ToolExpr):
    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_line(self)


class CounterExpr(ToolExpr):
    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_counter(self)
