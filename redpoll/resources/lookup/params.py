__all__ = ["ParamName", "types"]

from enum import StrEnum, auto

from redpoll.types import DataType


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
