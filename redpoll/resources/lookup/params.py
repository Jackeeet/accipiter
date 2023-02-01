__all__ = ["ParamName", "types", "default_values"]

from enum import StrEnum, auto

from redpoll.analyzer.token import Token, TokenKind
from redpoll.expressions import BinaryExpr, SideExpr
from redpoll.resources import keywords as kw
from redpoll.types import DataType, OpType


class ParamName(StrEnum):
    AREA = auto()
    COLOUR = auto()
    COUNTER = auto()
    DRAWABLE = auto()
    LINE = auto()
    MESSAGE = auto()
    NUMBER = auto()
    PERIOD = auto()
    SIDES = auto()
    SEGMENT = auto()
    TOOLS = auto()


types = {
    ParamName.AREA: {DataType.AREA},
    ParamName.COLOUR: {DataType.COLOUR},
    ParamName.COUNTER: {DataType.COUNTER},
    ParamName.DRAWABLE: {DataType.OBJECT_ID},
    ParamName.LINE: {DataType.LINE},
    ParamName.MESSAGE: {DataType.STRING},
    ParamName.NUMBER: {DataType.INT},
    ParamName.PERIOD: {DataType.INT},
    ParamName.SIDES: {DataType.SIDE},
    ParamName.SEGMENT: {DataType.SEGMENT},
    ParamName.TOOLS: {DataType.SEGMENT, DataType.ARC, DataType.AREA, DataType.LINE, DataType.COUNTER},
}

side_tokens = [
    (Token(TokenKind.SIDE, kw.SIDE_LEFT, -1, -1)),
    (Token(TokenKind.SIDE, kw.SIDE_RIGHT, -1, -1)),
    (Token(TokenKind.SIDE, kw.SIDE_TOP, -1, -1)),
    (Token(TokenKind.SIDE, kw.SIDE_BOTTOM, -1, -1))
]

default_values = {
    ParamName.SIDES: lambda _: BinaryExpr.from_list(side_tokens),
    ParamName.TOOLS: lambda components: BinaryExpr.from_list(components),
}
