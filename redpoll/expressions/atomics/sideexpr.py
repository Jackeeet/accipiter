from redpoll.analyzer.token import Token, TokenKind
from redpoll.expressions import ExpressionVisitor
from redpoll.expressions.atomics import AtomicExpr
from redpoll.types import DataType, Side
from redpoll.resources import keywords as kw


class SideExpr(AtomicExpr):
    def __init__(self, line: int, pos: int, side: Token) -> None:
        assert side.kind == TokenKind.SIDE
        match side.value:
            case kw.SIDE_BOTTOM:
                side = Side.BOTTOM
            case kw.SIDE_LEFT:
                side = Side.LEFT
            case kw.SIDE_RIGHT:
                side = Side.RIGHT
            case kw.SIDE_TOP:
                side = Side.TOP
            case _:
                raise ValueError("invalid side value")

        super().__init__(line, pos, side)

    @property
    def type(self) -> DataType:
        return DataType.SIDE

    def accept(self, visitor: ExpressionVisitor):
        visitor.visit_side(self)
