__all__ = ["required_params", "param_lists", "param_types", "part_types"]

from redpoll.resources import keywords as kw
from redpoll.types import DataType

_default_params = {kw.COLOUR, kw.THICKNESS}

""" Обязательные параметры для инструмента. """
required_params: dict[DataType, set[str]] = {
    DataType.POINT: {kw.POINT},
    DataType.SEGMENT: {kw.FROM, kw.TO},
    DataType.CURVE: {kw.CENTER, kw.RADIUS, kw.ANGLE_FROM, kw.ANGLE_TO},
    DataType.AREA: {kw.CONTENTS},
    DataType.LINE: {kw.CONTENTS},
    DataType.COUNTER: {kw.START, kw.STEP}
}

""" Допустимые параметры для инструмента. """
param_lists = {k: v.union(_default_params) if k != DataType.POINT else v
               for k, v in required_params.items()}

""" Допустимые типы данных для параметров инструментов. """
param_types = {
    kw.CONTENTS: {DataType.COMPOSITE},
    kw.FROM: {DataType.COORDS, DataType.POINT},
    kw.TO: {DataType.COORDS, DataType.POINT},
    kw.ANGLE_FROM: {DataType.INT},
    kw.ANGLE_TO: {DataType.INT},
    kw.POINT: {DataType.COORDS, DataType.TOOL_ID},
    kw.COLOUR: {DataType.COLOUR},
    kw.THICKNESS: {DataType.INT},
    kw.CENTER: {DataType.COORDS, DataType.POINT},
    kw.RADIUS: {DataType.INT},
    kw.START: {DataType.INT},
    kw.STEP: {DataType.INT}
}

""" Допустимые типы данных для частей составного инструмента. """
part_types = {DataType.SEGMENT, DataType.CURVE}
